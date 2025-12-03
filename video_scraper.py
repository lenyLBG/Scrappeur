"""
Video Stream Scraper - Détecte et capture automatiquement les flux vidéo
Supporte: Chrome, Firefox, Edge
"""

import json
import time
import logging
from typing import List, Dict, Set
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import TimeoutException
import requests
from fake_useragent import UserAgent

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VideoScraper:
    """Classe principale pour scraper les flux vidéo"""
    
    # Extensions de fichiers vidéo à détecter
    VIDEO_EXTENSIONS = {'.m3u8', '.mp4', '.webm', '.mpd', '.ts', '.m4s', '.mp3', '.m4a'}
    
    # Patterns d'URLs vidéo
    VIDEO_PATTERNS = [
        'manifest', 'playlist', 'segment', 'chunk', 
        'video', 'stream', 'media', 'hls', 'dash'
    ]
    
    def __init__(self, browser: str = 'chrome', headless: bool = False):
        """
        Initialise le scraper
        
        Args:
            browser: Type de navigateur ('chrome', 'firefox', 'edge')
            headless: Mode sans interface graphique
        """
        self.browser = browser.lower()
        self.headless = headless
        self.driver = None
        self.video_urls: Set[str] = set()
        self.ua = UserAgent()
        
    def _setup_chrome(self) -> webdriver.Chrome:
        """Configure Chrome avec interception réseau"""
        options = webdriver.ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless=new')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(f'user-agent={self.ua.random}')
        
        # Active la capture du trafic réseau
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _setup_firefox(self) -> webdriver.Firefox:
        """Configure Firefox avec interception réseau"""
        options = webdriver.FirefoxOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        options.set_preference('general.useragent.override', self.ua.random)
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def _setup_edge(self) -> webdriver.Edge:
        """Configure Edge avec interception réseau"""
        options = webdriver.EdgeOptions()
        
        if self.headless:
            options.add_argument('--headless=new')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-agent={self.ua.random}')
        
        # Active la capture du trafic réseau
        options.set_capability('ms:loggingPrefs', {'performance': 'ALL'})
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    def start(self):
        """Démarre le navigateur"""
        logger.info(f"Démarrage du navigateur {self.browser}...")
        
        try:
            if self.browser == 'chrome':
                self.driver = self._setup_chrome()
            elif self.browser == 'firefox':
                self.driver = self._setup_firefox()
            elif self.browser == 'edge':
                self.driver = self._setup_edge()
            else:
                raise ValueError(f"Navigateur non supporté: {self.browser}")
            
            logger.info(f"Navigateur {self.browser} démarré avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du démarrage du navigateur: {e}")
            raise
    
    def _is_video_url(self, url: str) -> bool:
        """
        Détermine si une URL correspond à un flux vidéo
        
        Args:
            url: URL à vérifier
            
        Returns:
            True si l'URL est un flux vidéo
        """
        url_lower = url.lower()
        
        # Vérifie les extensions
        if any(ext in url_lower for ext in self.VIDEO_EXTENSIONS):
            return True
        
        # Vérifie les patterns
        if any(pattern in url_lower for pattern in self.VIDEO_PATTERNS):
            return True
        
        return False
    
    def _extract_network_logs(self):
        """Extrait les URLs vidéo des logs réseau (Chrome/Edge uniquement)"""
        if self.browser not in ['chrome', 'edge']:
            return
        
        try:
            logs = self.driver.get_log('performance')
            
            for entry in logs:
                try:
                    log = json.loads(entry['message'])
                    message = log.get('message', {})
                    method = message.get('method', '')
                    
                    # Capture les requêtes réseau
                    if method == 'Network.requestWillBeSent':
                        params = message.get('params', {})
                        request = params.get('request', {})
                        url = request.get('url', '')
                        
                        if url and self._is_video_url(url):
                            self.video_urls.add(url)
                            logger.info(f"✓ Flux vidéo détecté: {url[:100]}...")
                    
                    # Capture les réponses réseau
                    elif method == 'Network.responseReceived':
                        params = message.get('params', {})
                        response = params.get('response', {})
                        url = response.get('url', '')
                        mime_type = response.get('mimeType', '')
                        
                        if url and (self._is_video_url(url) or 'video' in mime_type or 'mpegurl' in mime_type):
                            self.video_urls.add(url)
                            logger.info(f"✓ Flux vidéo détecté (réponse): {url[:100]}...")
                
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    continue
        
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des logs réseau: {e}")
    
    def _extract_video_elements(self):
        """Extrait les URLs des éléments vidéo HTML"""
        try:
            # Trouve les balises <video>
            video_elements = self.driver.find_elements(By.TAG_NAME, 'video')
            for video in video_elements:
                src = video.get_attribute('src')
                if src and self._is_video_url(src):
                    self.video_urls.add(src)
                    logger.info(f"✓ Élément vidéo trouvé: {src[:100]}...")
            
            # Trouve les balises <source>
            source_elements = self.driver.find_elements(By.TAG_NAME, 'source')
            for source in source_elements:
                src = source.get_attribute('src')
                if src and self._is_video_url(src):
                    self.video_urls.add(src)
                    logger.info(f"✓ Source vidéo trouvée: {src[:100]}...")
            
            # Trouve les iframes (peuvent contenir des vidéos)
            iframe_elements = self.driver.find_elements(By.TAG_NAME, 'iframe')
            for iframe in iframe_elements:
                src = iframe.get_attribute('src')
                if src:
                    logger.info(f"ℹ Iframe détecté: {src[:100]}...")
        
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des éléments vidéo: {e}")
    
    def scrape_page(self, url: str, wait_time: int = 10) -> List[str]:
        """
        Scrape une page pour détecter les flux vidéo
        
        Args:
            url: URL de la page à scraper
            wait_time: Temps d'attente pour le chargement (secondes)
            
        Returns:
            Liste des URLs de flux vidéo détectées
        """
        if not self.driver:
            self.start()
        
        logger.info(f"Chargement de la page: {url}")
        self.video_urls.clear()
        
        try:
            # Charge la page
            self.driver.get(url)
            
            # Attend le chargement
            logger.info(f"Attente de {wait_time} secondes pour le chargement complet...")
            time.sleep(wait_time)
            
            # Scroll pour déclencher le chargement lazy
            logger.info("Scroll de la page pour charger le contenu...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # Extrait les URLs vidéo
            logger.info("Analyse des flux réseau...")
            self._extract_network_logs()
            
            logger.info("Analyse des éléments HTML...")
            self._extract_video_elements()
            
            # Résultats
            if self.video_urls:
                logger.info(f"\n{'='*60}")
                logger.info(f"✓ {len(self.video_urls)} flux vidéo détecté(s)")
                logger.info(f"{'='*60}")
                for i, video_url in enumerate(self.video_urls, 1):
                    logger.info(f"{i}. {video_url}")
            else:
                logger.warning("Aucun flux vidéo détecté sur cette page")
            
            return list(self.video_urls)
        
        except Exception as e:
            logger.error(f"Erreur lors du scraping: {e}")
            return []
    
    def save_results(self, filename: str = 'video_urls.txt'):
        """
        Sauvegarde les URLs détectées dans un fichier
        
        Args:
            filename: Nom du fichier de sortie
        """
        if not self.video_urls:
            logger.warning("Aucune URL à sauvegarder")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Flux vidéo détectés - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n\n")
                for i, url in enumerate(self.video_urls, 1):
                    f.write(f"{i}. {url}\n")
            
            logger.info(f"✓ Résultats sauvegardés dans {filename}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
    
    def close(self):
        """Ferme le navigateur"""
        if self.driver:
            logger.info("Fermeture du navigateur...")
            self.driver.quit()
            self.driver = None
    
    def __enter__(self):
        """Support du context manager"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support du context manager"""
        self.close()


def main():
    """Fonction principale avec menu interactif"""
    print("="*60)
    print("VIDEO STREAM SCRAPER")
    print("="*60)
    print()
    
    # Choix du navigateur
    print("Choisissez un navigateur:")
    print("1. Chrome")
    print("2. Firefox")
    print("3. Edge")
    browser_choice = input("\nVotre choix (1-3): ").strip()
    
    browser_map = {'1': 'chrome', '2': 'firefox', '3': 'edge'}
    browser = browser_map.get(browser_choice, 'chrome')
    
    # Mode headless
    headless_choice = input("\nMode sans interface graphique? (o/n): ").strip().lower()
    headless = headless_choice == 'o'
    
    # URL à scraper
    url = input("\nEntrez l'URL de la page contenant la vidéo: ").strip()
    if not url.startswith('http'):
        url = 'https://' + url
    
    # Temps d'attente
    try:
        wait_time = int(input("\nTemps d'attente pour le chargement (secondes, défaut=10): ").strip() or "10")
    except ValueError:
        wait_time = 10
    
    print("\n" + "="*60)
    print("Démarrage du scraping...")
    print("="*60 + "\n")
    
    # Exécute le scraping
    try:
        with VideoScraper(browser=browser, headless=headless) as scraper:
            video_urls = scraper.scrape_page(url, wait_time)
            
            if video_urls:
                # Sauvegarde les résultats
                scraper.save_results()
                
                print("\n" + "="*60)
                print("RÉSULTATS")
                print("="*60)
                print(f"\n✓ {len(video_urls)} flux vidéo détecté(s)")
                print("\nLes URLs ont été sauvegardées dans 'video_urls.txt'")
                print("\nVous pouvez télécharger ces flux avec des outils comme:")
                print("- yt-dlp")
                print("- ffmpeg")
                print("- streamlink")
            else:
                print("\n⚠ Aucun flux vidéo détecté.")
                print("Vérifiez que la page contient bien une vidéo.")
    
    except KeyboardInterrupt:
        print("\n\n⚠ Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur: {e}")
        print(f"\n❌ Erreur: {e}")
    
    print("\nAppuyez sur Entrée pour quitter...")
    input()


if __name__ == "__main__":
    main()

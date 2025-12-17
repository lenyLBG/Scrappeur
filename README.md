# 🎥 Video Stream Scraper

Outil automatique de détection et capture de flux vidéo dans les navigateurs web (Chrome, Firefox, Edge).

## 🌟 Fonctionnalités

- ✅ **Multi-navigateurs**: Support de Chrome, Firefox et Edge
- ✅ **Détection automatique**: Intercepte les requêtes réseau pour capturer les flux vidéo
- ✅ **Formats multiples**: Détecte .m3u8, .mp4, .webm, .mpd, HLS, DASH, etc.
- ✅ **Mode headless**: Exécution sans interface graphique
- ✅ **Analyse HTML**: Détecte les balises `<video>` et `<source>`
- ✅ **Logs détaillés**: Enregistrement complet des opérations
- ✅ **Export**: Sauvegarde des URLs détectées
- ✅ **Scraping récursif**: Suit les liens automatiquement pour scraper plusieurs pages

## 📋 Prérequis

- Python 3.8+
- Un navigateur installé (Chrome, Firefox ou Edge)

## 🚀 Installation

1. Clonez ou téléchargez ce projet

2. Installez les dépendances:
```bash
pip install -r requirements.txt
```

Les drivers de navigateur seront téléchargés automatiquement au premier lancement.

## 💻 Utilisation

### Mode interactif (recommandé)

```bash
python video_scraper.py
```

Suivez les instructions à l'écran:
1. Choisissez le navigateur (Chrome, Firefox ou Edge)
2. Mode avec ou sans interface graphique
3. **Choisissez le mode de scraping**:
   - **Mode simple**: Scrape une seule page
   - **Mode récursif**: Suit les liens et scrape plusieurs pages
4. Entrez l'URL de la page contenant la vidéo
5. Définissez le temps d'attente pour le chargement
6. (Pour le mode récursif) Définissez la profondeur maximale et le délai entre les requêtes

### Mode programmation - Scraping simple

```python
from video_scraper import VideoScraper

# Utilisation basique
with VideoScraper(browser='chrome', headless=False) as scraper:
    video_urls = scraper.scrape_page('https://example.com/video-page', wait_time=10)
    scraper.save_results('mes_videos.txt')
    
    for url in video_urls:
        print(f"Flux vidéo trouvé: {url}")
```

### Mode programmation - Scraping récursif

```python
from video_scraper import VideoScraper

# Scrape récursivement plusieurs pages en suivant les liens
with VideoScraper(browser='chrome', headless=True) as scraper:
    video_urls = scraper.scrape_recursive(
        start_url='https://example.com',
        max_depth=2,                          # Profondeur maximale (0 = page actuelle, 1 = page + liens, etc.)
        wait_time=10,                         # Temps d'attente par page
        delay_between_requests=2,             # Délai entre les requêtes en secondes
        allowed_domains=['example.com']       # Domaines autorisés (None = domaine de départ uniquement)
    )
    
    scraper.save_results('toutes_les_videos.txt')
    print(f"Total: {len(video_urls)} flux vidéo détectés")
```

### Exemple avec configuration avancée

```python
from video_scraper import VideoScraper

# Chrome en mode headless
scraper = VideoScraper(browser='chrome', headless=True)
scraper.start()

try:
    # Scraping récursif avec options personnalisées
    print("Démarrage du scraping récursif...")
    urls = scraper.scrape_recursive(
        start_url='https://example.com/videos',
        max_depth=3,                                    # Explore jusqu'à 3 niveaux de profondeur
        wait_time=15,                                   # Attendre 15 secondes par page
        allowed_domains=['example.com', 'videos.example.com'],  # Plusieurs domaines autorisés
        delay_between_requests=3                        # 3 secondes entre les requêtes
    )
    
    print(f"✓ {len(urls)} flux vidéo détectés")
    scraper.save_results('resultats_complets.txt')
    
finally:
    scraper.close()
```

## 📁 Fichiers générés

- `video_urls.txt`: URLs des flux vidéo détectés
- `video_scraper.log`: Journal détaillé des opérations

## 🎯 Formats vidéo détectés

Le scraper détecte automatiquement:

- **Streaming adaptatif**: HLS (.m3u8), DASH (.mpd)
- **Vidéo standard**: .mp4, .webm, .avi, .mov
- **Segments**: .ts, .m4s
- **Audio**: .mp3, .m4a

## 🔧 Options avancées

### Méthode scrape_page

```python
scraper.scrape_page(
    url='https://example.com',  # URL à analyser
    wait_time=10                # Temps d'attente en secondes
)
```

### Méthode scrape_recursive

```python
scraper.scrape_recursive(
    start_url='https://example.com',     # URL de départ
    max_depth=2,                         # Profondeur maximale (0 = page actuelle)
    wait_time=10,                        # Temps d'attente par page (secondes)
    allowed_domains=None,                # Domaines autorisés (None = tous les domaines)
    delay_between_requests=2             # Délai entre les requêtes (secondes)
)
```

**Paramètres de scrape_recursive:**
- `max_depth`: 
  - `0` = Scrape uniquement la page de départ
  - `1` = Scrape la page de départ + les pages liées
  - `2` = Scrape la page de départ + les pages liées + les pages liées des pages liées
  - etc.
- `allowed_domains`: Limite le scraping à certains domaines (pour éviter de crawler le web entier)
- `delay_between_requests`: Respecte les serveurs en ajoutant un délai entre les requêtes

## 📝 Télécharger les vidéos détectées

Une fois les URLs détectées, utilisez:

### Avec yt-dlp (recommandé)
```bash
yt-dlp "url_du_flux"
```

### Avec ffmpeg
```bash
ffmpeg -i "url_du_flux.m3u8" -c copy video.mp4
```

### Avec streamlink
```bash
streamlink "url_de_la_page" best -o video.mp4
```

## 🛠️ Dépannage

### Le navigateur ne démarre pas
- Assurez-vous que le navigateur est installé
- Vérifiez votre connexion internet (pour télécharger les drivers)

### Aucun flux détecté
- Augmentez le `wait_time` (certaines pages mettent du temps à charger)
- Essayez un autre navigateur
- Désactivez le mode headless pour voir ce qui se passe
- Vérifiez que la page contient bien une vidéo

### Erreurs de permissions
- Exécutez en tant qu'administrateur si nécessaire
- Vérifiez les pare-feu et antivirus

## ⚠️ Limitations et avertissements

- **Usage légal uniquement**: Ne scrapez que du contenu dont vous avez le droit
- **Respect des robots.txt**: Vérifiez les conditions d'utilisation des sites
- **DRM**: Les contenus protégés ne peuvent pas être capturés
- **Performance**: Le mode headless est plus rapide mais peut manquer certains contenus

## 🤝 Contribution

Les contributions sont bienvenues! N'hésitez pas à:
- Signaler des bugs
- Proposer des améliorations
- Ajouter le support d'autres navigateurs

## 📄 Licence

Ce projet est fourni à des fins éducatives. Utilisez-le de manière responsable et légale.

## 🔗 Ressources utiles

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/)
- [streamlink](https://streamlink.github.io/)

---

**Note**: Ce scraper détecte les URLs de flux vidéo mais ne télécharge pas les vidéos automatiquement. Utilisez les outils mentionnés ci-dessus pour le téléchargement.

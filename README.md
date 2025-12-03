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
3. Entrez l'URL de la page contenant la vidéo
4. Définissez le temps d'attente pour le chargement

### Mode programmation

```python
from video_scraper import VideoScraper

# Utilisation basique
with VideoScraper(browser='chrome', headless=False) as scraper:
    video_urls = scraper.scrape_page('https://example.com/video-page', wait_time=10)
    scraper.save_results('mes_videos.txt')
    
    for url in video_urls:
        print(f"Flux vidéo trouvé: {url}")
```

### Exemple avec configuration avancée

```python
from video_scraper import VideoScraper

# Chrome en mode headless
scraper = VideoScraper(browser='chrome', headless=True)
scraper.start()

try:
    # Scrape plusieurs pages
    pages = [
        'https://example.com/video1',
        'https://example.com/video2'
    ]
    
    for page in pages:
        print(f"\nScraping: {page}")
        urls = scraper.scrape_page(page, wait_time=15)
        print(f"Trouvé: {len(urls)} flux vidéo")
    
    # Sauvegarde tous les résultats
    scraper.save_results('all_videos.txt')
    
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

### Paramètres de VideoScraper

```python
VideoScraper(
    browser='chrome',    # 'chrome', 'firefox', 'edge'
    headless=False       # True pour mode sans interface
)
```

### Méthode scrape_page

```python
scraper.scrape_page(
    url='https://example.com',  # URL à analyser
    wait_time=10                # Temps d'attente en secondes
)
```

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

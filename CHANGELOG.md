# CHANGELOG

## Version 2.0.0 - Scraping Récursif (2025-12-17)

### ✨ Nouvelles Fonctionnalités

#### 1. **Scraping Récursif** 🔄
- **Nouvelle méthode `scrape_recursive()`**: Permet de scraper automatiquement plusieurs pages en suivant les liens
- **Paramètre `max_depth`**: Contrôle la profondeur de récursion
  - `0` = page actuelle seulement
  - `1` = page actuelle + pages liées
  - `2` = et ainsi de suite...
- **Paramètre `allowed_domains`**: Limite le scraping à certains domaines pour éviter de crawler tout le web
- **Paramètre `delay_between_requests`**: Ajoute un délai respectueux entre les requêtes
- **Suivi automatique des liens**: Extraction et traitement récursif des liens trouvés

#### 2. **Nouvelles Méthodes**
- `_extract_links(url, allowed_domains)`: Extrait tous les liens d'une page avec filtrage par domaine
- Gestion des URLs relatives et absolues
- Stockage des pages visitées pour éviter les doublons

#### 3. **Interface Améliorée**
- Menu interactif avec choix entre mode simple et mode récursif
- Paramètres configurables pour le scraping récursif:
  - Profondeur maximale
  - Délai entre requêtes
- Affichage détaillé de la progression

#### 4. **Documentation Enrichie**
- README.md mis à jour avec exemples de scraping récursif
- Nouveau fichier `example_recursive_scraping.py` avec 6 exemples pratiques
- Documentation complète des paramètres

### 🔧 Améliorations Techniques

- Import centralisé de `urllib.parse` pour une meilleure gestion des URLs
- Nouvelles variables d'instance: `visited_urls`, `found_links`
- Logging détaillé de la progression du scraping récursif
- Affichage du nombre de pages visitées et de flux trouvés

### 📝 Exemples d'Utilisation

#### Mode Simple (comme avant)
```python
with VideoScraper(browser='chrome') as scraper:
    urls = scraper.scrape_page('https://example.com/video')
```

#### Mode Récursif (nouveau!)
```python
with VideoScraper(browser='chrome') as scraper:
    urls = scraper.scrape_recursive(
        start_url='https://example.com',
        max_depth=2,
        allowed_domains=['example.com'],
        delay_between_requests=2
    )
```

### 🎯 Cas d'Usage

1. **Extraire toutes les vidéos d'un site web**: Utilisez `max_depth=2` ou `3`
2. **Respecter les serveurs**: Utilisez `delay_between_requests=3` pour ajouter des délais
3. **Rester dans le domaine**: Utilisez `allowed_domains=['example.com']`
4. **Scraping rapide**: Utilisez `headless=True` et `max_depth=1`

### 📦 Compatibilité

- ✅ Python 3.8+
- ✅ Chrome, Firefox, Edge
- ✅ Windows, Linux, macOS
- ✅ Rétro-compatible avec l'ancienne méthode `scrape_page()`

### 🚀 Performance

- Scraping récursif optimisé pour limiter la consommation de ressources
- Délais configurables pour respecter les serveurs
- Mode headless pour une exécution plus rapide
- Stockage des URLs visitées pour éviter les doublons

### 📋 Fichiers Modifiés

- `video_scraper.py`: Ajout de la méthode `scrape_recursive()` et `_extract_links()`
- `README.md`: Documentation complète du scraping récursif
- `example_recursive_scraping.py`: Nouveau fichier avec 6 exemples pratiques

### ⚠️ Notes Importantes

- Le scraping récursif peut être gourmand en ressources et en temps
- Respectez toujours les conditions d'utilisation des sites
- Utilisez des délais appropriés (`delay_between_requests`) pour ne pas surcharger les serveurs
- L'option `allowed_domains` est fortement recommandée pour éviter de crawler involontairement d'autres sites

---

## Version 1.0.0 - Release Initial (2025)

### Fonctionnalités Initiales
- Support Chrome, Firefox, Edge
- Détection de flux vidéo (HLS, DASH, MP4, etc.)
- Mode headless
- Analyse HTML
- Logs détaillés
- Export des résultats

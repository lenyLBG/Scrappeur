"""
Guide d'utilisation rapide du scraping récursif
"""

# ==============================================================================
# GUIDE RAPIDE: SCRAPING RÉCURSIF
# ==============================================================================

# Option 1: Mode interactif (le plus simple)
# ===================================================
# $ python video_scraper.py
# 
# Puis sélectionnez:
# 1. Chrome/Firefox/Edge
# 2. Mode sans interface graphique? → o/n
# 3. Mode de scraping → 2 (Récursif)
# 4. Entrez l'URL: https://example.com
# 5. Temps d'attente: 10
# 6. Profondeur maximale: 2
# 7. Délai entre requêtes: 2


# Option 2: Script Python simple
# ===================================================

from video_scraper import VideoScraper

# Exemple 1: Scraping basique avec 2 niveaux de profondeur
print("Scraping récursif simple...")
with VideoScraper(browser='chrome', headless=True) as scraper:
    video_urls = scraper.scrape_recursive(
        start_url='https://example.com/videos',
        max_depth=2
    )
    print(f"Trouvé: {len(video_urls)} vidéos")
    scraper.save_results()


# Exemple 2: Scraping avancé avec tous les paramètres
print("\nScraping récursif avancé...")
with VideoScraper(browser='chrome', headless=True) as scraper:
    video_urls = scraper.scrape_recursive(
        start_url='https://example.com',
        max_depth=3,                        # Explore 3 niveaux
        wait_time=15,                       # Attendre 15 secondes par page
        allowed_domains=['example.com'],    # Rester sur example.com
        delay_between_requests=3            # 3 secondes entre les requêtes
    )
    print(f"Trouvé: {len(video_urls)} vidéos")
    scraper.save_results('advanced_results.txt')


# Paramètres expliqués
# =======================
# 
# start_url (obligatoire):
#   - L'URL de départ du scraping
#   - Exemple: 'https://example.com/videos'
#
# max_depth (défaut: 2):
#   - 0 = scrape uniquement la page de départ
#   - 1 = scrape la page + les pages liées
#   - 2 = scrape la page + les pages liées + les pages liées des pages liées
#   - ⚠️ Attention: 3+ peut être très long!
#
# wait_time (défaut: 10):
#   - Temps d'attente pour chaque page en secondes
#   - Augmentez si les vidéos se chargent lentement
#   - Minimum recommandé: 5 secondes
#
# allowed_domains (défaut: None):
#   - Limite le scraping à certains domaines
#   - Exemple: ['example.com', 'videos.example.com']
#   - None = scrape tous les domaines (attention!)
#   - Fortement recommandé pour éviter de crawler trop loin
#
# delay_between_requests (défaut: 2):
#   - Délai en secondes entre les requêtes
#   - Respecte les serveurs et évite les blocages
#   - Minimum recommandé: 1 seconde
#   - Augmentez si vous obtenez des erreurs de connexion


# Recommandations
# ================
#
# ✓ Pour un scraping RAPIDE:
#   max_depth=1, wait_time=5, delay_between_requests=1, headless=True
#
# ✓ Pour un scraping COMPLET:
#   max_depth=2, wait_time=10, delay_between_requests=2, headless=True
#
# ✓ Pour un scraping RESPECTUEUX (recommandé):
#   max_depth=2, wait_time=15, delay_between_requests=3, headless=True
#
# ✓ Pour un scraping APPROFONDI:
#   max_depth=3, wait_time=10, delay_between_requests=2, headless=True
#   + toujours utiliser allowed_domains!


# Troubleshooting
# ================
#
# ❌ "Aucun flux vidéo détecté"
#    → Augmentez wait_time (essayez 15 ou 20)
#    → Essayez headless=False pour voir ce qui se passe
#    → Vérifiez que la page contient bien une vidéo
#
# ❌ "Erreur de connexion"
#    → Augmentez delay_between_requests
#    → Vérifiez votre connexion internet
#    → Vérifiez que l'URL est correcte
#
# ❌ "Le scraping prend trop longtemps"
#    → Diminuez max_depth
#    → Diminuez wait_time (minimum 5)
#    → Utilisez headless=True
#    → Limitez allowed_domains
#
# ❌ "Trop de résultats non pertinents"
#    → Utilisez allowed_domains pour rester sur le bon site
#    → Diminuez max_depth
#    → Vérifiez votre configuration

print("\n✓ Guide chargé. Consultez ce fichier pour plus d'informations.")

"""
Exemples d'utilisation du scraping récursif
"""

from video_scraper import VideoScraper

# ============================================================================
# EXEMPLE 1: Scraping récursif simple
# ============================================================================
def example_basic_recursive():
    """Scraping récursif avec paramètres par défaut"""
    print("="*60)
    print("EXEMPLE 1: Scraping Récursif Simple")
    print("="*60)
    
    with VideoScraper(browser='chrome', headless=False) as scraper:
        # Scrape la page de départ et les pages liées (profondeur 2)
        video_urls = scraper.scrape_recursive(
            start_url='https://example.com/videos',
            max_depth=2
        )
        
        print(f"\n✓ Total: {len(video_urls)} flux vidéo détectés")
        scraper.save_results('example1_results.txt')


# ============================================================================
# EXEMPLE 2: Scraping récursif en mode headless (plus rapide)
# ============================================================================
def example_headless_recursive():
    """Scraping récursif sans interface graphique"""
    print("="*60)
    print("EXEMPLE 2: Scraping Récursif en Mode Headless")
    print("="*60)
    
    with VideoScraper(browser='chrome', headless=True) as scraper:
        video_urls = scraper.scrape_recursive(
            start_url='https://example.com',
            max_depth=1,                    # Explore seulement 1 niveau
            wait_time=5,                    # Attendre 5 secondes par page
            delay_between_requests=1        # 1 seconde entre les requêtes
        )
        
        print(f"\n✓ Total: {len(video_urls)} flux vidéo détectés")
        scraper.save_results('example2_results.txt')


# ============================================================================
# EXEMPLE 3: Scraping récursif avec domaines restreints
# ============================================================================
def example_restricted_domains():
    """Scraping récursif limité à certains domaines"""
    print("="*60)
    print("EXEMPLE 3: Scraping avec Domaines Restreints")
    print("="*60)
    
    with VideoScraper(browser='firefox', headless=True) as scraper:
        video_urls = scraper.scrape_recursive(
            start_url='https://example.com/media',
            max_depth=2,
            wait_time=10,
            # Limite le scraping à ces domaines seulement
            allowed_domains=['example.com', 'media.example.com'],
            delay_between_requests=2
        )
        
        print(f"\n✓ Total: {len(video_urls)} flux vidéo détectés")
        scraper.save_results('example3_results.txt')


# ============================================================================
# EXEMPLE 4: Scraping profond avec délais respectueux
# ============================================================================
def example_deep_recursive():
    """Scraping récursif profond avec délais entre les requêtes"""
    print("="*60)
    print("EXEMPLE 4: Scraping Profond avec Délais")
    print("="*60)
    
    with VideoScraper(browser='edge', headless=True) as scraper:
        video_urls = scraper.scrape_recursive(
            start_url='https://example.com',
            max_depth=3,                    # Explore 3 niveaux de profondeur
            wait_time=15,                   # Attendre 15 secondes par page
            delay_between_requests=3,       # 3 secondes entre les requêtes (respectueux)
            allowed_domains=['example.com']
        )
        
        print(f"\n✓ Total: {len(video_urls)} flux vidéo détectés")
        scraper.save_results('example4_results.txt')


# ============================================================================
# EXEMPLE 5: Comparaison simple vs récursif
# ============================================================================
def example_compare_simple_vs_recursive():
    """Compare le scraping simple avec le scraping récursif"""
    print("="*60)
    print("EXEMPLE 5: Comparaison Simple vs Récursif")
    print("="*60)
    
    url = 'https://example.com/videos'
    
    # Scraping simple
    print("\n1. Scraping SIMPLE (une seule page):")
    with VideoScraper(browser='chrome', headless=True) as scraper:
        simple_results = scraper.scrape_page(url, wait_time=10)
        print(f"   → {len(simple_results)} flux trouvés")
        scraper.save_results('simple_results.txt')
    
    # Scraping récursif
    print("\n2. Scraping RÉCURSIF (plusieurs pages):")
    with VideoScraper(browser='chrome', headless=True) as scraper:
        recursive_results = scraper.scrape_recursive(
            start_url=url,
            max_depth=2,
            wait_time=10
        )
        print(f"   → {len(recursive_results)} flux trouvés")
        scraper.save_results('recursive_results.txt')
    
    print(f"\n✓ Différence: {len(recursive_results) - len(simple_results)} flux additionnels trouvés")


# ============================================================================
# EXEMPLE 6: Scraping avec gestion d'erreurs complète
# ============================================================================
def example_with_error_handling():
    """Scraping récursif avec gestion complète des erreurs"""
    print("="*60)
    print("EXEMPLE 6: Scraping avec Gestion d'Erreurs")
    print("="*60)
    
    try:
        with VideoScraper(browser='chrome', headless=True) as scraper:
            print("Démarrage du scraping récursif...")
            
            video_urls = scraper.scrape_recursive(
                start_url='https://example.com',
                max_depth=2,
                wait_time=10,
                delay_between_requests=2
            )
            
            if video_urls:
                print(f"\n✓ Succès: {len(video_urls)} flux détectés")
                scraper.save_results('results_with_error_handling.txt')
                print("✓ Résultats sauvegardés")
            else:
                print("\n⚠ Aucun flux vidéo n'a été trouvé")
    
    except KeyboardInterrupt:
        print("\n⚠ Scraping interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du scraping: {e}")


if __name__ == "__main__":
    """Menu d'exécution des exemples"""
    import sys
    
    print("\n" + "="*60)
    print("EXEMPLES DE SCRAPING RÉCURSIF")
    print("="*60 + "\n")
    
    print("Choisissez un exemple à exécuter:")
    print("1. Scraping récursif simple")
    print("2. Scraping en mode headless")
    print("3. Scraping avec domaines restreints")
    print("4. Scraping profond avec délais")
    print("5. Comparaison simple vs récursif")
    print("6. Scraping avec gestion d'erreurs")
    print("0. Quitter")
    
    choice = input("\nVotre choix (0-6): ").strip()
    
    examples = {
        '1': example_basic_recursive,
        '2': example_headless_recursive,
        '3': example_restricted_domains,
        '4': example_deep_recursive,
        '5': example_compare_simple_vs_recursive,
        '6': example_with_error_handling,
    }
    
    if choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    elif choice != '0':
        print("\n❌ Choix invalide")
    
    print("\n")

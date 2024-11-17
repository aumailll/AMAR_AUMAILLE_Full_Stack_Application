# import scrapy
# import csv
# import os
# import html  # Importer le module html pour gérer les entités HTML

# # Fonction utilitaire pour nettoyer le texte
# def clean_text(text):
#     if text:
#         return ' '.join(text.split()).strip(' \n')
#     return ''

# class MyAnimeListSpider(scrapy.Spider):
#     name = 'anime'
#     allowed_domains = ['myanimelist.net']
#     start_urls = [
#         'https://myanimelist.net/topanime.php',
#         'https://myanimelist.net/topanime.php?limit=50',
#         'https://myanimelist.net/topanime.php?limit=100',
#         'https://myanimelist.net/topanime.php?limit=150',
#         'https://myanimelist.net/topanime.php?limit=200',
#         'https://myanimelist.net/topanime.php?limit=250',
#     ]

#     results = []  # Ajout d'une liste pour stocker les résultats

#     def __init__(self, *args, **kwargs):
#         super(MyAnimeListSpider, self).__init__(*args, **kwargs)
#         csv_file_path = r'D:\E5\Full_stack\anime_fullStack\Data\anime.csv'  # Chemin vers le fichier CSV
#         self.file = open(csv_file_path, 'w', newline='', encoding='utf-8')
#         self.writer = csv.writer(self.file, quoting=csv.QUOTE_ALL)  # Encapsuler tous les champs entre guillemets
#         # Écrire l'en-tête du CSV
#         self.writer.writerow(['Rank', 'Title', 'Link', 'Score', 'Episodes', 'Status', 'Studio', 'Producers', 'Type', 'Genres & Themes'])

#     def parse(self, response):
#         animes = response.css('.ranking-list')

#         for anime in animes:
#             item = {}
#             item['rank'] = anime.css('.rank span::text').get().strip()

#             title_element = anime.css('td.title a')
#             # Nettoyer le titre en utilisant html.unescape pour gérer les entités HTML
#             item['title'] = html.unescape(title_element.css('img::attr(alt)').get()).replace('Anime: ', '')  # Correction du format

#             item['link'] = title_element.css('::attr(href)').get()
#             score_label = anime.css('.score-label::text').get()
#             item['score'] = f"{score_label}"

#             yield scrapy.Request(url=item['link'], callback=self.parse_anime_page, meta={'item': item})

#     def parse_anime_page(self, response):
#         item = response.meta['item']

#         item['episodes'] = clean_text(response.xpath('//span[text()="Episodes:"]/following-sibling::text()').get())
#         item['statut'] = clean_text(response.xpath('//span[text()="Status:"]/following-sibling::text()').get())
#         item['studio'] = response.css('span:contains("Studios:") + a::text').getall()
#         item['producteurs'] = response.css('span:contains("Producers:") + a::text').getall()

#         blatest = response.css('span:contains("Genres:") + span[itemprop="genre"]::text , span[itemprop="genre"]::text').getall()
#         demographic = response.css('div.spaceit_pad span.dark_text:contains("Demographic:") + span[itemprop="genre"] + a::text').get()
#         item['type'] = demographic
#         item['genres_ET_themes'] = [g for g in blatest if g not in [demographic]]

#         # Ajouter l'item à la liste des résultats
#         self.results.append(item)

#     def closed(self, reason):
#         # Une fois que la spider est fermée, on trie les résultats par le champ 'rank' et on les écrit dans le fichier CSV
#         self.logger.info("-----------------------Spider fermée: tri des résultats en fonction du 'rank'.-----------------------")
#         self.results.sort(key=lambda x: int(x['rank']))

#         for result in self.results:
#             # Écrire chaque résultat dans le fichier CSV
#             self.writer.writerow([
#                 result['rank'],
#                 result['title'],  # Le titre est déjà nettoyé et peut contenir des caractères spéciaux
#                 result['link'],
#                 result['score'],
#                 result['episodes'],
#                 result['statut'],
#                 ', '.join(result['studio']),  # Joindre les studios en une seule chaîne
#                 ', '.join(result['producteurs']),  # Joindre les producteurs en une seule chaîne
#                 result['type'],
#                 ', '.join(result['genres_ET_themes']),  # Joindre les genres en une seule chaîne
#             ])

#         self.file.close()  # Fermer le fichier lors de la fermeture de la spider
#         self.logger.info(f"Les données ont été écrites dans {self.file.name}.")

# # notes attention des fois le type n est pas noté, il n y a pas demgraphic sur la page de l anime= info non renseignée



import scrapy
import html
import psycopg2
import os

def clean_text(text):
    if text:
        return ' '.join(text.split()).strip(' \n')
    return 'Non spécifié'  # Valeur par défaut si le texte est vide


class MyAnimeListSpider(scrapy.Spider):
    name = 'anime'
    allowed_domains = ['myanimelist.net']
    start_urls = [
        'https://myanimelist.net/topanime.php',
        'https://myanimelist.net/topanime.php?limit=50',
        'https://myanimelist.net/topanime.php?limit=100',
        'https://myanimelist.net/topanime.php?limit=150',
        'https://myanimelist.net/topanime.php?limit=200',
        'https://myanimelist.net/topanime.php?limit=250',
    ]

    def __init__(self, *args, **kwargs):
        super(MyAnimeListSpider, self).__init__(*args, **kwargs)
        self.connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            database=os.getenv('POSTGRES_DB', 'db_projet'),
            user=os.getenv('POSTGRES_USER', 'user'),
            password=os.getenv('POSTGRES_PASSWORD', 'password')
        )
        self.cursor = self.connection.cursor()

    def parse(self, response):
        """Scrape les informations générales sur les animes."""
        animes = response.css('.ranking-list')

        for anime in animes:
            item = {}
            item['rank'] = anime.css('.rank span::text').get().strip()
            title_element = anime.css('td.title a')
            item['title'] = html.unescape(title_element.css('img::attr(alt)').get()).replace('Anime: ', '')
            item['link'] = title_element.css('::attr(href)').get()
            item['score'] = anime.css('.score-label::text').get()

            self.logger.info(f"Anime extrait : {item}")

            yield scrapy.Request(
                url=item['link'],
                callback=self.parse_anime_page,
                meta={'item': item}
            )

    def parse_anime_page(self, response):
        """Scrape les informations détaillées sur un anime."""
        item = response.meta['item']

        item['episodes'] = clean_text(response.xpath('//span[text()="Episodes:"]/following-sibling::text()').get())
        item['status'] = clean_text(response.xpath('//span[text()="Status:"]/following-sibling::text()').get())
        item['studio'] = ', '.join(response.css('span:contains("Studios:") + a::text').getall())
        item['producers'] = ', '.join(response.css('span:contains("Producers:") + a::text').getall())

        genres = response.css('span:contains("Genres:") + span[itemprop="genre"]::text , span[itemprop="genre"]::text').getall()
        item['type'] = response.css('div.spaceit_pad span.dark_text:contains("Demographic:") + span[itemprop="genre"] + a::text').get() or 'Non spécifié'
        item['genres_and_themes'] = ', '.join(genres)

        self.logger.info(f"Détails de l'anime extrait : {item}")

        self.save_to_db(item)

    def save_to_db(self, item):
        """Sauvegarde un anime dans la base de données PostgreSQL."""
        query = """
            INSERT INTO anime (rank, title, link, score, episodes, status, studio, producers, type, genres_and_themes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (rank) DO NOTHING
        """
        data = (
            int(item['rank']),
            item['title'],
            item['link'],
            float(item['score']) if item['score'] else None,
            int(item['episodes']) if item['episodes'].isdigit() else None,
            item['status'],
            item['studio'],
            item['producers'],
            item['type'],
            item['genres_and_themes']
        )
       

        try:
            self.cursor.execute(query, data)
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Erreur lors de l'insertion dans la base de données : {e}")
            self.logger.error(f"Données problématiques : {data}")
            self.connection.rollback()

    def closed(self, reason):
        """Fermer la connexion à la base de données lors de l'arrêt du spider."""
        self.cursor.close()
        self.connection.close()
        self.logger.info("Connexion à la base de données fermée.")

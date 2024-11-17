import scrapy
import csv
import os
import html  # Importer le module html pour gérer les entités HTML

 # Fonction utilitaire pour nettoyer le texte
def clean_text(text):
     if text:
         return ' '.join(text.split()).strip(' \n')
     return ''

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

     results = []  # Ajout d'une liste pour stocker les résultats

     def __init__(self, *args, **kwargs):
         super(MyAnimeListSpider, self).__init__(*args, **kwargs)
         csv_file_path = r'D:\E5\Full_stack\Versions-projet\v7\Data\anime.csv'  # Chemin vers le fichier CSV
         self.file = open(csv_file_path, 'w', newline='', encoding='utf-8')
         self.writer = csv.writer(self.file, quoting=csv.QUOTE_ALL)  # Encapsuler tous les champs entre guillemets
         # Écrire l'en-tête du CSV
         self.writer.writerow(['rank', 'titre', 'lien', 'score', 'episodes', 'statut', 'studio', 'producteurs', 'type', 'genres_themes'])

     def parse(self, response):
         animes = response.css('.ranking-list')

         for anime in animes:
             item = {}
             item['rank'] = anime.css('.rank span::text').get().strip()

             title_element = anime.css('td.title a')
             # Nettoyer le titre en utilisant html.unescape pour gérer les entités HTML
             item['title'] = html.unescape(title_element.css('img::attr(alt)').get()).replace('Anime: ', '')  # Correction du format

             item['link'] = title_element.css('::attr(href)').get()
             score_label = anime.css('.score-label::text').get()
             item['score'] = f"{score_label}"

             yield scrapy.Request(url=item['link'], callback=self.parse_anime_page, meta={'item': item})

     def parse_anime_page(self, response):
         item = response.meta['item']

         item['episodes'] = clean_text(response.xpath('//span[text()="Episodes:"]/following-sibling::text()').get())
         item['statut'] = clean_text(response.xpath('//span[text()="Status:"]/following-sibling::text()').get())
         item['studio'] = response.css('span:contains("Studios:") + a::text').getall()
         item['producteurs'] = response.css('span:contains("Producers:") + a::text').getall()

         blatest = response.css('span:contains("Genres:") + span[itemprop="genre"]::text , span[itemprop="genre"]::text').getall()
         demographic = response.css('div.spaceit_pad span.dark_text:contains("Demographic:") + span[itemprop="genre"] + a::text').get()
         item['type'] = demographic
         item['genres_ET_themes'] = [g for g in blatest if g not in [demographic]]

         # Ajouter l'item à la liste des résultats
         self.results.append(item)

     def closed(self, reason):
         # Une fois que la spider est fermée, on trie les résultats par le champ 'rank' et on les écrit dans le fichier CSV
         self.logger.info("-----------------------Spider fermée: tri des résultats en fonction du 'rank'.-----------------------")
         self.results.sort(key=lambda x: int(x['rank']))

         for result in self.results:
             # Écrire chaque résultat dans le fichier CSV
             self.writer.writerow([
                 result['rank'],
                 result['title'],  # Le titre est déjà nettoyé et peut contenir des caractères spéciaux
                 result['link'],
                 result['score'],
                 result['episodes'],
                 result['statut'],
                 ', '.join(result['studio']),  # Joindre les studios en une seule chaîne
                 ', '.join(result['producteurs']),  # Joindre les producteurs en une seule chaîne
                 result['type'],
                 ', '.join(result['genres_ET_themes']),  # Joindre les genres en une seule chaîne
             ])

         self.file.close()  # Fermer le fichier lors de la fermeture de la spider
         self.logger.info(f"Les données ont été écrites dans {self.file.name}.")

#notes attention des fois le type n est pas noté, il n y a pas demgraphic sur la page de l anime= info non renseignée




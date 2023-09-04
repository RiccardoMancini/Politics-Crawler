# Twitter scraper
Attività di ricerca finalizzata alla creazione di uno scraper per la raccolta di dati relativi alle elezioni politiche 2022 in Italia, al fine di sviluppare un dataset completo.
### Keywords utilizzate
- 'enricoletta', 'partitodemocratico', 'pdnetwork'
- 'giorgiameloni', 'fratelliditalia', 'meloni'
- 'matteosalvini', 'legasalvini', 'matteosalvinimi', 'salvini'
- 'berlusconi', 'forza_italia'
- 'giuseppeconte', 'mov5stelle', 'movimento5stelle', 'GiuseppeConteIT'

### Esempio formato JSON dei tweet estratti
```
{
   "_id": 1571836155380858881,
   "author": 123920914,
   "text": "#EnricoLetta la accusa di esaltare il #patriarcato? La fulminante replica di #GiorgiaMeloni: \"Quei testi li scrivi tu? O hai perso il senso della misura o paghi chi ti detesta\"  https://t.co/7PbMykvLtc https://t.co/Lgjr4TV4PK",
   "media_url": [
      "https://pbs.twimg.com/media/FdBIp3pWQAIaM-0?format=jpg&name=large"
   ],
   "reaction": {
      "n_like": 111,
      "n_reply": 25,
      "n_retweet": 13,
      "n_quote": 1
   },
   "keyword": [
      "enricoletta",
      "giorgiameloni"
   ]
},

{
   "_id": 1572619156071108608,
   "author": 1040271648082067458,
   "text": "L'#Italia ha bisogno di credibilit\\xc3\\xa0 economica e istituzionale. Il #presidenzialismo \\xc3\\xa8 in grado di garantire la stabilit\\xc3\\xa0 necessaria.@FratellidItalia @GiorgiaMeloni https://t.co/UjtjojPAMr",
   "media_url": [
      "https://pbs.twimg.com/media/FdMQxzcWIAci6FS?format=jpg&name=large"
   ],
   "reaction": {
      "n_like": 100,
      "n_reply": 8,
      "n_retweet": 10,
      "n_quote": 0
   },
   "keyword": [
      "giorgiameloni",
      "fratelliditalia"
   ]
},

{
   "_id": 1572935694414417921,
   "author": 529247064,
   "text": "Tra poco saremo a Piazza del popolo, con il Presidente Berlusconi, per la grande manifestazione del centrodestra. @forza_italia sar\\xc3\\xa0 presente con i suoi militanti e dirigenti. Sventoliamo alta la nostra bandiera, domenica siamo pronti a tornare alla guida del Paese! https://t.co/Oa78Yjb6I8",
   "media_url": [
      "https://pbs.twimg.com/media/FdQwrURWAAQS3Ki?format=jpg&name=large"
   ],
   "reaction":{
      "n_like": 46,
      "n_reply": 27,
      "n_retweet": 16,
      "n_quote": 1
   },
   "keyword": [
      "berlusconi",
      "forza_italia"
   ]
}
```
### Esempio formato "authors"
```
{
   "_id": 123920914,
   "username": "Libero_official",
   "desc": "liberoquotidiano.it",
   "follower": 322571,
   "following": 73,
   "n_statuses": 209306,
   "n_favourites": 37,
   "n_media": 27439
},

{
   "_id": 1040271648082067458,
   "username": "carettamc11",
   "desc": "Politica Governo & Istituzioni, deputata di @FratellidItalia.",
   "follower": 2083,
   "following": 270,
   "n_statuses": 6560,
   "n_favourites": 3267,
   "n_media": 3211
},

{
   "_id": 529247064,
   "username": "Antonio_Tajani",
   "desc": "Presidente della Commissione Affari Costituzionali del @Europarl_IT, Coordinatore nazionale di @forza_italia e Vicepresidente del Partito Popolare Europeo @EPP",
   "follower": 77360,
   "following": 3628,
   "n_statuses": 16413,
   "n_favourites": 7170,
   "n_media": 4947
}
```

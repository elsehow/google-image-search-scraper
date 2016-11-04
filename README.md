# google image search scraper

`python scraper.py --query="cute pandas" --n=100`

Will get the first 100 google image results for "cute pandas" in a directory `cute pandas/[time of query]/`. That directory will contain a file `query-results.json` with metadata, along with 100 cute panda images, named by result index + filename

You'll also need a file in this directory called `keys.json` with the format

```json
{
  "developerKey": "your google developer key",
  "cx": "you google custom search id - cse.google.com/cse/manage/all"
}

```

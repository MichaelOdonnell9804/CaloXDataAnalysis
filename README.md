# CaloXDataAnalysis

Download the data file from [here](https://yofeng.web.cern.ch/yofeng/CaloX/)

Change the path in `data/datafiles.json`

```
python3 prepareDQMPlots.py
python3 makeDQMPlots.py
```

## Event display generation

You can create event display PNGs and an HTML viewer with
`makeEventDisplays.py`. The script supports sampling options so the output
HTML can show a random subset of events.

```bash
python3 makeEventDisplays.py your_file.root \
    --random-per-block 1 --block-size 100 --nth-interval 20
```

The example above selects one random event in every block of 100 events and
also includes every 20th event.
# CaloXDataAnalysis
# CaloXDataAnalysis
# CaloXDataAnalysis
# CaloXDataAnalysis
# CaloXDataAnalysis
# CaloXDataAnalysis
# CaloXDataAnalysis

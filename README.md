# Gigapan Downloader 2

> New: Much faster download due to using the same session across multiple downloads parallelizing the downloads.

Python **3** script for downloading gigapan pictures

This script should be used to only download gigapan tiles that you have copyright permissions to use.  Doing otherwise is a violation of the [Terms of Service of Gigapan, Inc.](http://www.gigapan.com/cms/about/terms) and is expressly prohibited.

This Python **3.X** script downloads gigapan pictures at their highest resolution.

## Install

```
git clone https://github.com/flekschas/gigapan-downloader
cd gigapan-downloader
# We recommend setting up a viirtual environment first. E.g.:
# mkvirtualenv -a $(pwd) gigapan-downloader
pip install -r ./requirements.txt
```


## How to run?
```
python downloadGigaPan.py <image-id> <start-height> <start-width>
```

For example:

To download http://www.gigapan.com/gigapans/54825 use the `<image-id>` 54825 and call the script as follows:

```
python downloadGigaPan.py 54825
```

This will download the image tiles into directory "54825"

User snapshots(tags) locations and descriptions can be found at :

```
http://www.gigapan.com/gigapans/<imageid>/snapshots.json
```

This software is made available for research and non-commercial use only.

### Citation
Saliency-Assisted Navigation of Very Large Landscape Images<br />
C.Y. Ip, and A. Varshney<br />
IEEE Transactions on Visualization and Computer Graphics, 17(12), 2011, pp 1737 - 1746.<br />

```
@article{ ip2011saliency,
    title={Saliency-assisted navigation of very large landscape images},
    author={Ip, C.Y. and Varshney, A.},
    journal={IEEE Transactions on Visualization and Computer Graphics},
    volume={17},
    number={12},
    pages={1737--1746},
    year={2011},
}
```

https://youtu.be/FwSMjYHTNX8

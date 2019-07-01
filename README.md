# image-compressor

Compresses images.

# Usage

In order to **compress** an image use the following command:

```
$ python3 compressor.py -c image.png image.bin
```

To **decompress** an image use the following command:

```
$ python3 compressor.py -x image.bin image2.png
```

# Benchmarks

This approach was tested with the [Rawzor's Image Compression Benchmark](https://imagecompression.info/test_images/).

The current performarnce is below optimized `png` with `optipng`:

| image                          |  comp. ratio |  png ratio |
| :----------------------------- | -----------: | ---------: |
| cathedral.ppm                  |    1.773578  |   1.948486 |
| bridge.ppm                     |    1.567508  |   1.691269 |
| spider_web.ppm                 |    3.547640  |   3.817402 |
| nightshot_iso_1600.ppm         |    1.633340  |   1.774391 |
| hdr.ppm                        |    2.589867  |   2.879170 |
| nightshot_iso_100.ppm          |    2.809052  |   3.084504 |
| big_building.ppm               |    1.792917  |   1.913515 |
| leaves_iso_200.ppm             |    1.681106  |   1.783960 |
| artificial.ppm                 |    5.879867  |  11.426134 |
| leaves_iso_1600.ppm            |    1.496978  |   1.593128 |
| big_tree.ppm                   |    1.633181  |   1.728946 |
| flower_foveon.ppm              |    3.164391  |   3.299397 |
| fireworks.ppm                  |    3.817746  |   3.916710 |
| deer.ppm                       |    1.433505  |   1.510089 |
| **mean**                       |    1.78325   |    1.93100 |

To download the dataset, run:
```
bash benchmark_download.sh
```

To reproduce the results, run:
```
bash benchmark_download.sh
```

To get the previous table, run:
```
bash benchmark_download.sh
```

[![Contributors][contributors-shield]][contributors-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


# arithmetic_coding


<p align="center">
    <img src="https://raw.githubusercontent.com/scresh/arithmetic_coding/master/images/slow-cooker.png" alt="Logo" width="128" height="128">

  <h3 align="center">Arithmetic coding</h3>

  <p align="center">
    Implementation of lossless data compression technique written in Python.
  </p>
</p>

## About The Project

App created as a student project work for Data Compression course at the Warsaw University of Technology.

Due to the use of fraction module in computing, the performance tends to be slow for larger files.

## Usage

Use -h or --help flags to get automatically generated help text for the command-line program:
```bash
$./arithmetic_coding.py --help
usage: arithmetic_coding.py [-h] {compress,decompress} input output

Compress/Decompress files using arithmetic coding algorithm.

positional arguments:
  {compress,decompress}
  input
  output

optional arguments:
  -h, --help            show this help message and exit
```

## Screenshots

![](https://raw.githubusercontent.com/scresh/arithmetic_coding/master/images/example_usage.png)


<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/badge/contributors-1-orange.svg?style=flat-square
[contributors-url]: https://github.com/scresh/arithmetic_coding/graphs/contributors
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/emanuel-zarzecki/

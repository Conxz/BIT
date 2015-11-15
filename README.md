# BIT

The Brain Imaging Toolkit (BIT) is a collection of Python tools for analysis of both publicly available and private brain imaging data.

## Installation

Dependencies:

* FSL
* Nipype
* FreeSurfer

...

## Datasets

* NKI, [Nathan Kline Institute(NKI)/Rockland Sample](http://fcon_1000.projects.nitrc.org/indi/pro/nki.html)

* NSP, [Neo-Spearman Project(NSP)](http://www.brainactivityatlas.org/about-baa/overview/), also known as Gene, Environment, Brain, and Behavior(GEB<sup>2</sup>)

## Problematic data

* NKI

	1351931, incorrect bvec file for DTI64_1.

	2136756, incorrect directions for DTI64_1 scanning, maybe incomplete scanning.
	
	9421819, 4230470, poor data quality for structrual MRI (maybe caused by large motion) (see /doc/nki_poormri_*.jpg). 

## License information

Copyright (c) 2015-2015, BIT Developers All right reserved.

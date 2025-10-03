
# normalizacija / izdvajanje h&e komponenti

    1. https://scikit-image.org/docs/0.25.x/api/skimage.color.html#skimage.color.separate_stains skimage separate stains
    2. https://web.archive.org/web/20160624145052/http://www.mecourse.com/landinig/software/cdeconv/cdeconv.html
    3. https://d1wqtxts1xzle7.cloudfront.net/40705455/AnalQuantCytHist-AR-libre.pdf?1449652785=&response-content-disposition=inline%3B+filename%3DQuantification_of_histochemical_staining.pdf&Expires=1759267488&Signature=cdS3cOf~9OGUVtTaVWSmiYE7QBZytr-N6Balv~3NfmK0ilxx2VkR4YeopZNbbaULEgrfqh0MZnq4UMCB4kl51fqlMuWWO7WJXKk-DxhLzBZkKzamea93Bmf0MLp2XF3oJOUlZMwvMixSpyHWlsARj6CKSIUyEWVrOYK5aho47vh4rJjpWR-cWxRJlB4Wgor6SXVlFkDjFZZQ81zZd4~I9sfc~ecjQIIeTuS54Ct9g1cmElhKsxa9NMqjp3lO7z59WT96D2pKDpe0PpoL068hkzvqe7bu~mbkCg4rgPI9724sPx77AHARTLQ76gxumxIvNaxiY1WTdz5HxX-Ehmc~-w__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA
    4. https://sci-hub.se/https://doi.org/10.1364/JOSAA.15.002036
    5. https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf
    6. https://github.com/bnsreenu/python_for_microscopists/blob/master/303%20-%20Reinhard%20color%20transformation%E2%80%8B/303-Reinhard%20color_transfer.py
    7. 


    A. Color Normalization
One of the first steps essential for both fluorescent and bright
field microscopy image analysis is color and illumination nor-
malization. This process reduces the differences in tissue sam-
ples due to variation in staining and scanning conditions. The
illumination can be corrected either using calibration targets or
estimating the illumination pattern from a series of images by
fitting polynomial surfaces [29]. Another approach is to match
the histograms of the images. Software that corrects for spec-
tral and spatial illumination variations is becoming a standard
package provided by most bright field manufacturers. This is
an essential step for algorithms that heavily depend on color
space computations. Yang and Foran [53] presented a robust
color-based segmentation algorithm for histological structures
that used image gradients estimated in the LUV color space to
deal with issues of stain variability. In the next section, we give
detailed description of correcting another artifact, tissue autoflu-
orescence, in fluorescent images.
[53]    https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=1504818&casa_token=qj5G-NCHqvQAAAAA:5b74brkCvqGi-wGN4_w0NCSOyIQ6_VFOcI8UphTJOSBnyaQxvUXuEsQww_3EkEwvupODnjhcuuE&tag=1
[29]    https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=4540989&casa_token=r9yNdc10S5kAAAAA:rQmRTM0DC6Lb0o1wvr6PjL51hJPlrLh29JY7cjwsohJ5GHcpWddaz0H2fv09I08DKu3E9xVxI0A



# dobri radovi
neki watershed based
https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0070221&type=printable

kao neko poredjenje
https://sci-hub.se/https://doi.org/10.1016/j.neucom.2019.09.083

post-processing (odvajanje spojenih kontura)
https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7300433



# bitno
- poredjenje neuralnih https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7300433
- neki survey (msm da je los rad) https://link.springer.com/content/pdf/10.1007/s12530-023-09491-3.pdf
- yolo i nas dataset https://ieeexplore.ieee.org/abstract/document/10470849

# nebitno
- neki post-processing https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7300433
- jos neki post-processing https://www.researchgate.net/profile/Tuomas-Eerola/publication/300124111_Segmentation_of_Partially_Overlapping_Nanoparticles_Using_Concave_Points/links/572c413408aef7c7e2c6be4a/Segmentation-of-Partially-Overlapping-Nanoparticles-Using-Concave-Points.pdf
- dobar review ali star https://sci-hub.se/10.1109/RBME.2009.2034865
- aktivne konture https://sci-hub.se/10.1109/TMI.2012.2190089
- csgo(2025) https://pmc.ncbi.nlm.nih.gov/articles/PMC12305447/pdf/nihms-2084568.pdf
- 

# ja implementiram
- ja implementiram https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0070221&type=printable
- frst https://ieeexplore.ieee.org/document/1217601
- color deconv https://www.academia.edu/18183623/Quantification_of_histochemical_staining_by_color_deconvolution
- morphological reconstruction https://ieeexplore.ieee.org/document/217222, https://www.mathworks.com/help/images/understanding-morphological-reconstruction.html
- imhmin https://www.mathworks.com/help/images/ref/imhmin.html
- 
- 




# NOTES
- max vrednosti slike budu bas bas male posle morfoloskih operacija
    mozda treba da se rescaleuje nesto ili nmp ne znam ni sto su tako male treba proveriti
- 


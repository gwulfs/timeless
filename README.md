**Timeless - hackharvard**
===================
By [Arpit Agarwal](http://clweb.csa.iisc.ernet.in/cse12/arpit.agarwal), [David van IJzendoorn](http://www.researchgate.net/profile/David_Van_Ijzendoorn), and [Gideon Wulfsohn](http://gwulfs.github.io)

---

Inspired by [recent work](http://techcrunch.com/2014/07/24/your-smartphone-will-soon-know-if-you-have-bipolar-disorder) from the University of Michigan, we built an app that accesses our model which we trained on Wikipedia pages suggested by CMU's [NELL](http://rtw.ml.cmu.edu/rtw/) Knowledge Engine to visualize disease severity scores given symptoms extracted from an unstructured textual input.

While previous pipelines for accessing similar metrics for specific diseases exist, we sought out to build a more generalized model which leverages tf-idf vectors in a bayesian setting on a broader corpus.

![demo](http://i.imgur.com/k1WA9L6.png?1)

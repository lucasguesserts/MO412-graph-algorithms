# Wikipedia Requests for Adminship (with text)

One obtained this data in the [SNAP repository of Stanford](https://snap.stanford.edu/data/wiki-RfA.html). The description below has been copied from the source page.

## Dataset information

For a Wikipedia editor to become an administrator, a [request for adminship (RfA)](http://en.wikipedia.org/wiki/Wikipedia:RfA) must be submitted, either by the candidate or by another community member. Subsequently, any Wikipedia member may cast a supporting, neutral, or opposing vote.

We crawled and parsed all votes since the adoption of the RfA process in 2003 through May 2013. The dataset contains 11,381 users (voters and votees) forming 189,004 distinct voter/votee pairs, for a total of 198,275 votes (this is larger than the number of distinct voter/votee pairs because, if the same user ran for election several times, the same voter/votee pair may contribute several votes).

This induces a directed, signed network in which nodes represent Wikipedia members and edges represent votes. In this sense, the present dataset is a more recent version of the Wikipedia adminship election data. However, there is also a rich textual component in RfAs, which was not included in the older version: each vote is typically accompanied by a short comment (median/mean: 19/34 tokens). A typical positive comment reads, _"I've no concerns, will make an excellent addition to the admin corps"_, while an example of a negative comment is, _"Little evidence of collaboration with other editors and limited content creation."_

| Network statistics |         |
|--------------------|---------|
| Nodes              | 10,835  |
| Edges              | 159,388 |
| Triangles          | 956,428 |

The above statistics were computed after transforming the data into a directed network. The number of edges (159,388) is smaller than the number of voter/votee pairs (189,004) because neutral votes were discarded in the network we used for computing the statistics (but they are included in the dataset).

## Data format

```txt
TGT:Lord Roem
VOT:1
RES:1
YEA:2013
DAT:19:53, 25 January 2013
TXT:'''Support''' per [[WP:DEAL]]: clueful, and unlikely to break Wikipedia.
```

where entries are separated by a single empty line and:

* `SRC`: user name of source, i.e., voter;
* `TGT`: user name of target, i.e., the user running for election;
* `VOT`: the source's vote on the target (-1 = oppose; 0 = neutral; 1 = support);
* `RES`: the outcome of the election (-1 = target was rejected as admin; 1 = target was accepted);
* `YEA`: the year in which the election was started;
* `DAT`: the date and time of this vote;
* `TXT`: the comment written by the source, in [wiki markup](http://en.wikipedia.org/wiki/Help:Wiki_markup);

## References

Robert West, Hristo S. Paskov, Jure Leskovec, and Christopher Potts: [Exploiting Social Network Structure for Person-to-Person Sentiment Analysis](http://infolab.stanford.edu/~west1/pubs/West-Paskov-Leskovec-Potts_TACL-14.pdf). Transactions of the Association for Computational Linguistics, 2 (Oct): 297-310, 2014.

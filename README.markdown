Lightly structured Eurovision data
==================================

A set of [TOML](https://toml.io) files describing the scoring behind the
Eurovision Song Contest, originally used by the 
[eurovisiondrinking](https://github.com/norm/eurodrink) website and twitter bot.

## Terms used

* *Country* — A country that participates in Eurovision.
* *Contest* — A whole Eurovision Song Contest event in a given year.
* *Show* — An individual live show in a Contest (eg first semi-final).
* *Artist* — One or more Singers (and any other musicians/performers) that
  perform a Song in a Show.
* *Singer* — An individual singer that is or is part of an Artist.
* *Song* — A song, as performed by an Artist, to represent a Country in a
  Contest.
* *Performance* — A Song, performed in a Show.
* *Score* — A number of points awarded by a Country to a Performance, either
  by a jury or a televote.


## Data files

* `contests.toml`

    A list of Contest entries. Contains the host Country, and a list of
    Shows.

    ```toml
    [1956]
    host  = 'switzerland'
    shows = ['1956-final']
    ```

* `countries.toml`

    A set of Country entries, that have taken part in the Eurovision Song
    Contest. Contains the English version of the country's name, and the
    hashtag recognised by Twitter when using "hashflags" to decorate the tweet
    with that country's flag (normally the same as the [three-letter country
    code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3))

    ```toml
    [austria]
    english = 'Austria'
    hashtag = 'AUT'
    ```

* `artists/__year__.toml`

    A list of Artist entries, arranged by the first year of the Contest in
    which they appeared. Contains 

    ```toml
    [birthe-wilke-gustav-winckler]
    name   = 'Birthe Wilke & Gustav Winckler'
    singer = [
        'birthe-wilke',
        'gustav-winckler',
    ]
    ```

* `singers/__year__.toml`

    A list of Singer entries, arranged by the first year of the Contest in
    which they appeared. Contains their name, the more common name they
    performed under if applicable, the date of their birth and death if known,
    and a list of citizenships.

    ```toml
    [gustav-winckler]
    name        = 'Gustav Frands Wilzeck Winckler'
    known_as    = 'Gustav Winckler'
    born        = 1925-10-13
    died        = 1979-01-20
    citizenship = ['denmark']
    ```

* `songs/__year__.toml`

    A list of Song entries, arranged by the year of the Contest in which they
    were performed. Contains the title, the performing Artist and the Country
    that the song represented in the Contest.

    ```toml
    [skibet-skal-sejle-i-nat]
    title   = 'Skibet skal sejle i nat'
    artist  = 'birthe-wilke-gustav-winckler'
    country = 'denmark'
    ```

* `shows/__year__.toml`

    A list of Show entries, arranged by the year of the Contest they form.
    Contains the type of show, the date it occured, and a list of Song
    performances in the order they were performed.

    ```toml
    [1957-final]
    date         = 1957-03-03
    type         = 'final'
    performances = [
        'straatdeuntje',
        'amours-mortes-tant-de-peine',
        'all',
        'corde-della-mia-chitarra',
        'wohin-kleines-pony',
        'net-als-toen',
        'telefon-telefon',
        'la-belle-amour',
        'skibet-skal-sejle-i-nat',
        'lenfant-que-jetais',
    ]
    ```

* `scores/__year__-__show_type__.toml`

    A list of Score entries, arranged by the year of the Contest in which
    they were awarded and the type of Show they were awarded in. Contains
    an array of Score entries for each awarding Country, each Score
    containing the Song, the points awarded, and the source of the points
    ("jury" or "televote").

    ```toml
    [[austria]]
    song   = 'all'
    points = 1
    source = 'jury'

    [[belgium]]
    song   = 'net-als-toen'
    points = 5
    source = 'jury'

    [[belgium]]
    song   = 'la-belle-amour'
    points = 2
    source = 'jury'
    ```
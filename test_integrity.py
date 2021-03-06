import datetime
import toml


class TestCountryIntegrity:
    def setup_class(self):
        self.countries = toml.load('countries.toml')

    def test_countries(self):
        for country in self.countries:
            entry = self.countries[country]
            assert 'english' in entry 
            assert entry['english']
            assert 'hashtag' in entry
            assert entry['hashtag']
            assert 'language' in entry
            assert len(entry['language']) > 0


class TestContestIntegrity:
    def setup_class(self):
        self.countries = toml.load('countries.toml')
        self.contests = toml.load('contests.toml')

    def test_contests(self):
        for contest in self.contests:
            assert int(contest)
            assert int(contest) > 1955
            assert int(contest) < 2022
            entry = self.contests[contest]
            assert 'host' in entry
            assert entry['host']
            assert self.countries[entry['host']]
            assert 'shows' in entry
            assert len(entry['shows']) > 0


class TestSingerIntegrity:
    def setup_class(self):
        self.countries = toml.load('countries.toml')
        self.contests = toml.load('contests.toml')

    def test_singers(self):
        existing_singers = {}

        for contest in self.contests:
            new_singers = toml.load('singers/%s.toml' % contest)
            for singer in new_singers:
                entry = new_singers[singer]

                assert singer not in existing_singers
                existing_singers[singer] = entry

                assert 'name' in entry
                assert entry['name']

                assert 'citizenship' in entry
                assert len(entry['citizenship']) > 0
                for country in entry['citizenship']:
                    assert country in self.countries

                if 'born' in entry:
                    assert type(entry['born']) == datetime.date
                    assert entry['born'] != datetime.date(1901, 1, 1)
                if 'died' in entry:
                    assert type(entry['died']) == datetime.date
                    assert entry['died'] != datetime.date(1901, 1, 1)


class TestArtistIntegrity:
    def setup_class(self):
        self.countries = toml.load('countries.toml')
        self.contests = toml.load('contests.toml')
        self.singers = {}
        for contest in self.contests:
            new_singers = toml.load('singers/%s.toml' % contest)
            self.singers.update(new_singers)

    def test_artists(self):
        existing_artists = {}

        for contest in self.contests:
            new_artists = toml.load('artists/%s.toml' % contest)
            for artist in new_artists:
                entry = new_artists[artist]

                assert artist not in existing_artists
                existing_artists[artist] = entry

                assert 'name' in entry
                assert entry['name']

                assert 'singer' in entry
                assert len(entry['singer']) > 0
                for singer in entry['singer']:
                    assert singer in self.singers


class TestSongIntegrity:
    def setup_class(self):
        self.countries = toml.load('countries.toml')
        self.languages = []
        for country in self.countries:
            for language in self.countries[country]['language']:
                self.languages.append(language)
        self.contests = toml.load('contests.toml')
        self.singers = {}
        self.artists = {}
        for contest in self.contests:
            new_singers = toml.load('singers/%s.toml' % contest)
            self.singers.update(new_singers)
            new_artists = toml.load('artists/%s.toml' % contest)
            self.artists.update(new_artists)

    def test_songs(self):
        existing_songs = {}

        for contest in self.contests:
            new_songs = toml.load('songs/%s.toml' % contest)
            songs_per_country = {}
            for song in new_songs:
                entry = new_songs[song]

                assert song not in existing_songs
                existing_songs[song] = entry

                assert 'title' in entry
                assert entry['title']

                assert 'artist' in entry
                assert entry['artist']
                assert entry['artist'] in self.artists

                assert 'language' in entry
                assert entry['language']
                assert len(entry['language']) > 0
                for language in entry['language']:
                    assert language in self.languages

                assert 'country' in entry
                country = entry['country']
                assert country
                assert country in self.countries
                try:
                    songs_per_country[country] += 1
                except KeyError:
                    songs_per_country[country] = 1

            if contest == '1956':
                for country in songs_per_country:
                    assert songs_per_country[country] == 2
            if contest != '1956':
                for country in songs_per_country:
                    assert songs_per_country[country] == 1


class TestSingerArtistIntegrity:
    def setup_class(self):
        self.countries = toml.load('countries.toml')
        self.contests = toml.load('contests.toml')
        self.singers = {}
        self.artists = {}
        self.songs = {}
        for contest in self.contests:
            new_singers = toml.load('singers/%s.toml' % contest)
            self.singers.update(new_singers)
            new_artists = toml.load('artists/%s.toml' % contest)
            self.artists.update(new_artists)
            new_songs = toml.load('songs/%s.toml' % contest)
            self.songs.update(new_songs)

    def test_singer_artist_combo(self):
        seen_singers = []
        for artist in self.artists:
            for singer in self.artists[artist]['singer']:
                assert singer in self.singers
                seen_singers.append(singer)
        for singer in self.singers:
            assert singer in seen_singers


class TestShowIntegrity:
    def setup_class(self):
        self.countries = toml.load('countries.toml')
        self.contests = toml.load('contests.toml')
        self.singers = {}
        self.artists = {}
        self.songs = {}
        for contest in self.contests:
            new_singers = toml.load('singers/%s.toml' % contest)
            self.singers.update(new_singers)
            new_artists = toml.load('artists/%s.toml' % contest)
            self.artists.update(new_artists)
            new_songs = toml.load('songs/%s.toml' % contest)
            self.songs.update(new_songs)

    def test_shows(self):
        for contest in self.contests:
            shows = toml.load('shows/%s.toml' % contest)

            valid_shows = {'%s-final' % contest}

            for show in shows:
                assert show in valid_shows

                entry = shows[show]
                assert 'date' in entry
                assert type(entry['date']) == datetime.date
                assert entry['date'].year == int(contest)

                assert 'performances' in entry
                assert len(entry['performances']) > 0
                for performance in entry['performances']:
                    assert performance in self.songs


class TestScoresIntegrity:
    def setup_class(self):
        self.countries = toml.load('countries.toml')
        self.contests = toml.load('contests.toml')
        self.singers = {}
        self.artists = {}
        self.songs = {}
        self.shows = {}
        for contest in self.contests:
            new_singers = toml.load('singers/%s.toml' % contest)
            self.singers.update(new_singers)
            new_artists = toml.load('artists/%s.toml' % contest)
            self.artists.update(new_artists)
            new_songs = toml.load('songs/%s.toml' % contest)
            self.songs.update(new_songs)
            new_shows = toml.load('shows/%s.toml' % contest)
            self.shows.update(new_shows)

    def test_scores(self):
        for show in self.shows:
            year = int(show.split('-')[0])
            scores = toml.load('scores/%s.toml' % show)
            for country in scores:
                assert country in self.countries
                total = 0

                for score in scores[country]:
                    assert 'song' in score
                    assert score['song'] in self.songs

                    assert 'points' in score
                    points = score['points']
                    assert type(points) == int
                    total += points

                    assert points > 0
                    if year == 1956:
                        pass
                    elif year >= 1957 and year <= 1961:
                        assert points <= 10
                    elif year == 1962:
                        assert points in (1, 2, 3)
                    elif year == 1963:
                        assert points in (1, 2, 3, 4, 5)
                    elif year >= 1964 and year <= 1966:
                        assert points in (1, 3, 5, 6, 9)
                    elif year >= 1967 and year <= 1970:
                        assert points >= 1
                        assert points <= 10
                    else:
                        raise UnknownYear

                    assert 'source' in score
                    assert score['source'] in ['jury', 'televote']

                if year == 1956:
                    pass
                elif year >= 1957 and year <= 1961:
                    assert total == 10
                elif year == 1962:
                    assert total == 6
                elif year == 1963:
                    assert total == 15
                elif year >= 1964 and year <= 1966:
                    assert total == 9
                elif year >= 1967 and year <= 1970:
                    assert total == 10
                else:
                    raise UnknownYear

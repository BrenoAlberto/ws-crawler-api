from ws.pageobjects.BasePage import BasePage
from scrapy import Selector
from time import sleep


class TrackPage(BasePage):
    def __init__(self, browser):
        BasePage.__init__(self, browser)

    _locator_dictionary = {
        "samples_section": '//span[@class="section-header-title" and contains(text(), "Contains sample")]/../..',
        "sampled_section": '//span[@class="section-header-title" and contains(text(), "Was sampled")]/../..',
        "covers_section": '//span[@class="section-header-title" and contains(text(), "Was covered")]/../..',
        "track_name": '//*[contains(@class, "trackName")]/text()',
        "artist_name": '//*[contains(@class, "trackArtist")]/a[1]/text()',
        "track_blocks": '//div[@class="trackDetails"]',
    }

    # That’s-a-Rack That's-a-Rack
    def get_track_page(self, artist, track):
        artist = self._slugify(artist)
        track = self._slugify(track)
        self.browser.get(f"https://www.whosampled.com/{artist}/{track}/")

    def _get_track_data(self, track_block):
        track_block = Selector(text=track_block.extract())
        return {
            "artist": track_block.xpath(self._locator_dictionary["artist_name"]).get(),
            "track": track_block.xpath(self._locator_dictionary["track_name"]).get(),
        }

    def _get_track_blocks(self, section_block):
        return section_block.xpath(self._locator_dictionary["track_blocks"])

    def _get_section_data(self, page_source, section_name):
        tracks_data = []

        if self.exists(self._locator_dictionary[section_name]):
            section = Selector(
                text=(
                    page_source.xpath(self._locator_dictionary[section_name])[
                        0
                    ].extract()
                )
            )

            track_blocks = self._get_track_blocks(section)

            for track_block in track_blocks:
                tracks_data.append(self._get_track_data(track_block))

        return tracks_data

    def get_samples(self):
        sleep(2)
        page_source = Selector(text=self.browser.page_source)

        samples_data = self._get_section_data(page_source, "samples_section")
        sampled_data = self._get_section_data(page_source, "sampled_section")
        covers_data = self._get_section_data(page_source, "covers_section")
        sleep(2)

        return {
            "samples_data": samples_data,
            "sampled_data": sampled_data,
            "covers_data": covers_data,
        }

    @staticmethod
    def _slugify(text):
        return "-".join(_ for _ in (text.split(" ")))

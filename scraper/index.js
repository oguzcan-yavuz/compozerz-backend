const cheerio = require('cheerio');
const axios = require('axios');
const Constants = require('./constants');
const fs = require('fs');
const path = require('path');

const scrapeComposerFromMidiWorld = async (composer) => {
	const { data } = await axios({
		baseURL: Constants.MIDIWORLD_URL,
		url: `/${composer.toLowerCase()}.htm`,
		method: 'get',
		responseType: 'document'
	});

	return data;
};

const isMidExtension = str => /\.mid$/.test(str);

const getAllLinksFromDoc = (doc) => {
	const $ = cheerio.load(doc);
	const links = $('a');
	let parsedLinks = [];
	$(links).each((i, link) => {
		parsedLinks.push($(link).attr('href'));
	});

	return parsedLinks;
};

const scrapeMidisOfComposer = async (composer) => {
	console.log(`scraping midi urls of composer: ${composer}`);
	const doc = await scrapeComposerFromMidiWorld(composer);
	const links = getAllLinksFromDoc(doc);
	const midiLinks = links.filter(isMidExtension);
	console.log(`scraped midi link count for ${composer} is: ${midiLinks.length}`);

	return midiLinks;
};

const getMidiNameFromUrl = url => url.split('/').pop();

const createDirIfNotExists = dir => {
	if (!fs.existsSync(dir)){
		fs.mkdirSync(dir);
	}
};

const createDirForComposer = composer => {
	const dir = path.resolve(__dirname, '..', 'data');
	const composerDir = path.resolve(dir, composer.toLowerCase(), 'midi');
	createDirIfNotExists(composerDir);

	return composerDir;
};

const getMidisOfComposer = async (composer) => {
	const midiUrlsOfComposer = await scrapeMidisOfComposer(composer);

	return Promise.all(midiUrlsOfComposer.map(url => {
		const midiName = getMidiNameFromUrl(url);
		const dirPath = createDirForComposer(composer);
		const midiPath = path.resolve(dirPath, midiName);
		console.log(`downloading midi: ${midiName}`);

		return axios({
			method: "get",
			url,
			responseType: "stream"
		}).then((response) => {
			response.data.pipe(fs.createWriteStream(midiPath));
		});
	}));
};

(async () => {
	return await Promise.all(Constants.COMPOSER_NAMES.map(getMidisOfComposer)).then(res => console.log('ALL IS DONE!'))
})();

let kyteParams = {
	utm_campaign: window.location.pathname,
	referrer: document.referrer
};

const kyteAnalyticsKeys = [
	'aid',
	'kid',	
	'pkid',	
	'cid',
	'email',
	'fbclid',
	'gclid',
	'bento_visitor_id'
];
        
function getKid(params = {}, onLoad = function(){}) {
	// Parametros para adicionar ao post
	if(Object.keys(params).length > 0)
		for(let k in params) {
			kyteParams[k] = params[k]
			localStorage.setItem(k, params[k])
		}
	kyteAnalyticsKeys.forEach(function(k){
		if(!kyteParams[k]){
			let value = localStorage.getItem(k);
			if(!!value && value !== 'undefined') kyteParams[k] = value;
		}
	});	

	let cookie = document.cookie.split(';');
	cookie.forEach(function(v){
		let p = v.trim().split('=');
		let k = (p[0] === '_ga' ? 'cid' : p[0])
		if(kyteAnalyticsKeys.indexOf(k) !== -1 && !kyteParams[k] && !!p[1] && !!p[1] !== 'undefined') kyteParams[k] = p[1];
	});	
	if(kyteAnalyticsKeys.every(k => (!kyteParams[k]))){
  		let uid = new ShortUniqueId({ length:15 });
		kyteParams.pkid = uid() + Date.now()
		localStorage.setItem('pkid', kyteParams.pkid)
	}

	// Cancela o envio de dados se kyte-analytics houver match
	let aidMatchDate = localStorage.getItem('aidMatchDate');
	if(!!aidMatchDate && aidMatchDate !== 'undefined') kyteParams.aidMatchDate = aidMatchDate

	// Adiciona todos os parâmetros em LocalStorage
	for(var k in kyteParams) {
		localStorage.setItem(`k_${k}`, kyteParams[k])
	}
	dataLayer.push({ event:"AttributionDataUpdated" })	

	if(!!aidMatchDate && aidMatchDate !== 'undefined'){
		if(kyteParams.kid) onLoad(kyteParams.kid)
		return
	}

	let xhrReceive = new XMLHttpRequest();
	xhrReceive.open('post', 'https://kyte-api-gateway.azure-api.net/get-kyte-id');
	xhrReceive.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
	xhrReceive.onreadystatechange = function(){
		if(xhrReceive.readyState === XMLHttpRequest.DONE){
			if(xhrReceive.responseText) {
				let kidResult = JSON.parse(xhrReceive.responseText);
				let kid = kidResult.kid
				if(localStorage.getItem('kid') !== kid) {
					kyteParams.kid = kid 
					localStorage.setItem('kid', kid)
					// Enviar para serviÃ§o GTM
					if(typeof (dataLayer) === 'object') dataLayer.push({ event:"KidIdentify", kid: kid })
				}
				if(kidResult.aidMatchDate) localStorage.setItem('aidMatchDate', kidResult.aidMatchDate)
				onLoad(kid);
			}
		}
	};
	xhrReceive.send(JSON.stringify(kyteParams));
}

function addParams(url, keys) {
    let localKeys = { ...keys }
    let i = url.indexOf('?')
    if(i === -1) return url
    let domain = url.substr(0, i)
    let params = url.substr(++i)
    let urlParts = params.split('&');
    urlParts.forEach((v, k) => {
        let p = v.split('=');
        if(p[0] === 'link'){
            urlParts[k] = `link=${encodeURIComponent(addParams(decodeURIComponent(p[1]), keys))}`
        } else if(p[0] !== 'url' && localKeys[p[0]]) {
            urlParts[k] = `${p[0]}=${localKeys[p[0]]}`
            delete localKeys[p[0]]
        }
    });
    for(let p in localKeys) if(p !== 'url') urlParts.push(`${p}=${localKeys[p]}`)
    return `${domain}?${urlParts.join('&')}`
}


(function(){
	if(typeof ShortUniqueId !== 'function') {
		throw new Error('kyte-analytics.js precisa do modulo https://github.com/simplyhexagonal/short-unique-id')
	}
	// Bloqueio do serviço
	if(
		window.location.href.indexOf('kyte.link') !== -1 ||
		window.location.href.indexOf('kyte.com.br/ajuda') !== -1 ||
		window.location.href.indexOf('appkyte.com/ayuda') !== -1 ||
		window.location.href.indexOf('kyteapp.com/help') !== -1
	) return

	let urlParams = location.search.substring(1).split('&');
	urlParams.forEach(function(v){
		let p = v.split('=');
		if (!!p[1] && p[1] !== 'undefined') {
			kyteParams[p[0]] = decodeURI(p[1]);
			if(p[0] === 'kid') localStorage.setItem('kid', p[1])
		}
	});	

	getKid({ url: (window.location.href || '') }, function(kid){
		let fields = document.getElementsByTagName('input')
		for(let f of fields){
			var name = f.getAttribute('name')
			if (name && kyteParams[name]) { f.value = kyteParams[name]; }
		}
		let domain = document.location.href
		let links = document.getElementsByTagName('a')
		for(aTag of links) {
			if(aTag.href.indexOf(domain) === -1) aTag.href = addParams(aTag.href, kyteParams)
		}
	})
	
})();

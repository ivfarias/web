/**
 * Gerencia pequenos formulários, fazendo sua validação e aplicando recurso de "passos"
 */

const initLeadForm = function(id = 'LeadForm', validationRules = {}){
	var alias = `leadScript_${id}`
	var setVisible = function(elm, isVisible) {
		elm.setAttribute('class', `${elm.getAttribute('class').replace('hidden', '')} ${isVisible ? 'show' : 'hidden'}`)
	}
	var validate = function(step){
		var elm = step
		? window[alias].form.getElementsByClassName(`step${step}`)[0]
		: window[alias].form
		var fields = elm.getElementsByTagName('*')
		for(var f of fields){
		var name = f.getAttribute('name')
		if(
			(f.hasAttribute('required') && ((f.type === 'checkbox' && !f.checked) || !!!f.value)) ||
			(validationRules[name] && !validationRules[name](f.value))
			) return false
		}
		return true
	}
	var showStep = function(step){
		if(step > window[alias].steps || step < 1) return
		window[alias].currStep = step
		for(var s=1; s<=window[alias].steps; s++)
		setVisible(window[alias].form.getElementsByClassName(`step${s}`)[0], (step === s))
		setVisible(window[alias].prevBtn, (step > 1))
		setVisible(window[alias].nextBtn, (step < window[alias].steps))
		setVisible(window[alias].submitBtn, (step === window[alias].steps))
	}
	window[alias] = {
		form: document.getElementById(id),
		steps: Number(document.getElementById(id).getAttribute('data-steps')),
		submitBtn: document.getElementById(id).getElementsByClassName('btn-submit')[0]
	}
	window[alias].submitBtn.addEventListener('click', function(evt){
		evt.preventDefault()
		if(!validate()) return false
		window[alias].form.submit()
		window[alias].submitBtn.disabled = true
	});    
	if(window[alias].steps > 0){
		window[alias].prevBtn = window[alias].form.getElementsByClassName('btn-prev')[0]
		window[alias].nextBtn = window[alias].form.getElementsByClassName('btn-next')[0]
		window[alias].prevBtn.addEventListener('click', function(evt){ evt.preventDefault(); showStep(window[alias].currStep - 1); })
		window[alias].nextBtn.addEventListener('click', function(evt){ evt.preventDefault(); if(validate(window[alias].currStep)) showStep(window[alias].currStep + 1); })
		showStep(1)
	}
}

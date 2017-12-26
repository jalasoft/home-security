
const ServerProxy = {};

ServerProxy.csrfToken = document.querySelector("form input[type=hidden]").value;

ServerProxy.login = function(password) {
	return fetch("/home-security/login/", {
	    method: 'POST',
	    headers: {
			"X-CSRFToken": this.csrfToken
		},
	    body: password
	}).then(response => {
		if (response.ok) {
			var securityToken = response.headers.get("X-SECURE-TOKEN");
			localStorage.setItem("SecurityToken", securityToken);
		}
		
		return response;
	});
}

ServerProxy.logout = function() {
	return fetch("/home-security/logout/", {
		method: 'POST',
		headers: {
			"X-CSRFToken": this.csrfToken,
			"X-SECURE-TOKEN": localStorage.getItem("SecurityToken")
		}
	}).then(response => {
		localStorage.removeItem("SecurityToken");
		return response;
	});
}

ServerProxy.isSessionValid = function() {
	const token = localStorage.getItem("SecurityToken");
	if (!token) {
		return Promise.resolve(false);
	}
	
	return fetch("/home-security/validateToken/", {
		method: "GET",
		headers: new Headers({
			"X-SECURE-TOKEN": token
		})
	}).then(
		response => {
			if (response.ok) {
				return Promise.resolve(true);
			}
			
			return Promise.resolve(false);
		}
	);
}

ServerProxy.captureArea = function(area, refresh, encoding) {
	const finalEncoding = encoding ? encoding : '';
	const url = `/home-security/camera/${area}?refresh=${refresh}&encoding=${finalEncoding}`;
	
	return fetch(url, {
			headers: {
				"X-SECURE-TOKEN": localStorage.getItem("SecurityToken")
			},
			method: "GET"
		}
	);
}





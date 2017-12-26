function LoginController(parentController, loginFragment) {
	
	console.log("initializing login controller");
	
	Controller.call(this, "login", parentController, [], loginFragment);
	
	this.form = this.rootElement.querySelector("form");
	this.form.addEventListener("submit", this.onLogin.bind(this));
	
	this.passwordField = this.rootElement.querySelector("#pwd");
	this.passwordField.addEventListener("input", this.disableIfEmpty.bind(this));
	
	this.loginButton = this.rootElement.querySelector("form button");
		
	this.disableIfEmpty();
}

Object.setPrototypeOf(LoginController.prototype, Controller.prototype);

LoginController.prototype.disableIfEmpty = function(t) {
	const disabled = this.passwordField.value.length == 0;
	
	if (disabled) {
		this.validInputField();
	}
	this.loginButton.disabled = disabled;
}

LoginController.prototype.onLogin = function(e) {
	e.preventDefault();
	
	const passwordValue = this.passwordField.value;
	ServerProxy.login(passwordValue)
	.then(response => {
		if (response.ok) {
			this.dispatchEvent("login", {});
		} else {
			this.invalidInputField();
		}
	});
}

LoginController.prototype.invalidInputField = function() {
	this.passwordField.style.backgroundColor = "red";
}


LoginController.prototype.validInputField = function() {
	this.passwordField.style.backgroundColor = "black";
}



function CameraController(parentController, root) {
	
		Controller.call(this, "camera", parentController, [], root);
	
		this.area = root.dataset["area"];
	    console.log(`Initializing camera controller for view '${this.area}'.`); 
	
		this.refreshImg = root.querySelector(".refresh");
		this.captureImg = root.querySelector(".capture");
		this.titleSpan = root.querySelector(".description .area");
		this.timestampSpan = root.querySelector(".description .timestamp");
	
		this.titleSpan.innerHTML = this.area;

		this.refreshImg.addEventListener("click", this.captureFreshView.bind(this));
		this.captureImg.addEventListener("click", this.openNewTabWithCapture.bind(this));
		this.captureImg.style.cursor = 'pointer';
	}
	
	Object.setPrototypeOf(CameraController.prototype, Controller.prototype);

	/* PROTOTYPE STUFF */

	CameraController.prototype.show = function() {
		this.captureHistoricalView()
		.then(r => {
			Controller.prototype.show.call(this);
		});
	}

	CameraController.prototype.openNewTabWithCapture = function() {
		let imageUrl = this.captureImg.src;
		window.open(imageUrl, this.area);
	}

	CameraController.prototype.captureFreshView = function() {
		this.fetchAndDisplay(true);	
	}

	CameraController.prototype.captureHistoricalView = function() {
		return this.fetchAndDisplay(false);
	}

	CameraController.prototype.fetchAndDisplay = function(refresh) {
		var url = this.captureUrl(refresh, "base64");
		console.log(`Capturing a fresh image for camera ${this.area} from ${url}.`); 
		
		this.startProgressAnimation();
		
		return ServerProxy.captureArea(this.area, refresh, "base64")
		.then(r => {
			if (r.status == 200) {
				this.displayView(r)
			}
			else if (r.status == 401) {
				this.dispatchEvent("unauthorized", {});
			} else {
				Promise.reject("Unexpected rasponse: " + r.status);
			}
		})
		.catch(this.displayError.bind(this));
	}
	
	CameraController.prototype.captureUrl = function(refresh, encoding) {
		const finalEncoding = encoding ? encoding : '';
		
		return `/home-security/camera/${this.area}?refresh=${refresh}&encoding=${finalEncoding}`;
	}
	
	CameraController.prototype.displayView = function(response) {
		this.stopProgressAnimation();
		
		response.text().then(text => {
			this.captureImg.src = "data:image/jpeg;base64," + text;
		});
		
		this.titleSpan.innerHTML = this.area;
		this.timestampSpan.innerHTML = response.headers.get("X-SNAPSHOT-CREATED-ISO");
	}
	
	CameraController.prototype.displayError = function(error) {
		this.stopProgressAnimation();
		
		console.log(error);
		this.captureImg.innerHTML = error.message;
	}
	
	CameraController.prototype.startProgressAnimation = function() {
		this.refreshImg.classList.add("progress-running");
		this.refreshImg.classList.remove("progress-paused");
	}
	
	CameraController.prototype.stopProgressAnimation = function() {
		this.refreshImg.classList.remove("progress-running");
		this.refreshImg.classList.add("progress-paused");
	}

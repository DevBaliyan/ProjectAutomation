// Create a listener to catch all network requests
let originalOpen = XMLHttpRequest.prototype.open;
let originalSend = XMLHttpRequest.prototype.send;
window.requestData = [];

// Override the open method to capture the URL
XMLHttpRequest.prototype.open = function(method, url) {
    this._url = url;
    this._method = method;
    return originalOpen.apply(this, arguments);
};

// Override the send method to capture the request data
XMLHttpRequest.prototype.send = function(data) {
    if (this._url.includes('questionSubmit')) {
        console.log('Intercepted request to: ' + this._url);
        
        // Save the request data
        window.requestData.push({
            url: this._url,
            method: this._method,
            data: data
        });
        
        // Add an event listener to check the response
        this.addEventListener('load', function() {
            console.log('Request completed with status: ' + this.status);
        });
    }
    return originalSend.apply(this, arguments);
};

// Function to retrieve all captured requests
window.getInterceptedRequests = function() {
    return window.requestData;
};

console.log('Request interceptor installed');

function Progress(el) {
    this.el = el;
    this.loading = 0;
    this.loaded = 0;
  }
  
  /**
   * Increment the count of loading tiles.
   */
  Progress.prototype.addLoading = function () {
    ++this.loading;
    this.update();
  };
  
  /**
   * Increment the count of loaded tiles.
   */
  Progress.prototype.addLoaded = function () {
    var _this = this;
    // setTimeout(function () {
        ++this.loaded;
        _this.update();
    // }, 100);
  };
  
  /**
   * Update the progress bar.
   */
  Progress.prototype.update = function () {
    const width = ((this.loaded / this.loading) * 100).toFixed(1) + '%';
    this.el.style.width = width;

    if (this.loaded === this.loading) {
        this.hide();
        this.loaded = 0;
        this.loading = 0;
        this.show();
        var event = new Event('loadEnd');
        this.el.dispatchEvent(event);
    }
  };
  
  /**
   * Show the progress bar.
   */
  Progress.prototype.show = function () {
    this.el.style.visibility = 'visible';
  };
  
  /**
   * Hide the progress bar.
   */
  Progress.prototype.hide = function () {
    const style = this.el.style;
    setTimeout(function () {
      style.visibility = 'hidden';
      style.width = 0;
    }, 250);
  };
  
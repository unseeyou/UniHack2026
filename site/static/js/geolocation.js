/**
 * 
 * @param {PositionOptions?=} options
 * @returns {Promise<GeolocationPosition>}
 */
export function getPosition(options) {
    return new Promise((res, rej) => navigator.geolocation.getCurrentPosition(res, rej, options));
}

/**
 * 
 * @param {PositionCallback} callback 
 * @param {ErrorCallback?=} errorCallback 
 * @param {PositionOptions?=} options 
 * @returns {{ cancel(): void }}
 */
export function watchPosition(callback, errorCallback, options) {
    const id = navigator.geolocation.watchPosition(callback, errorCallback, options);
    return {
        cancel() {
            navigator.geolocation.clearWatch(id);
        }
    }
}

var reloading;

function checkReloading() {
    if (window.location.hash=="#autoreload") {
        reloading=setTimeout("window.location.reload();", 5000);
        document.getElementById("reloadCB").checked=true;
    }
}

function toggleAutoRefresh(cb) {
    if (cb.checked) {
        window.location.replace("#autoreload");
        reloading=setTimeout("window.location.reload();", 5000);
    } else {
        window.location.replace("#");
        clearTimeout(reloading);
    }
}

function isHttps(){
    return (document.location.protocol == 'https:');
}

window.onload=checkReloading;


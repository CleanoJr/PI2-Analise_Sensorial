firebase.auth().onAuthStateChanged(user => {
    if (!user) {
        window.location.href = "../../home.html";
    }
})
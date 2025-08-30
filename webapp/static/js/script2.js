
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



async function onClick(event) {
    event.preventDefault();
    const link = event.currentTarget;
    const url = link.href;

    try {
        const response = await makeRequest(url);

        if (response.action === "added") {
            link.textContent = "удалить из избранных";
        } else if (response.action === "removed") {
            link.textContent = "добавить в избранное";
        }


    } catch (err) {
        console.error(err);
    }


function onLoad(){
    let links = document.querySelectorAll('[data-fav="album"]');
    for (let link of links){
        link.addEventListener('click', onClick);
    }

}

window.addEventListener("load", onLoad);}
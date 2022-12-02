function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
function deleteNote(noteId){
let csrftoken = getCookie('csrftoken');

fetch('/delete-note', {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken,
                "Accept": "network/json",
                "Content-Type": "network/json",
            },
            body: JSON.stringify({noteId: noteId})
}).then((_res) => {
    window.location.href = "/";})
}
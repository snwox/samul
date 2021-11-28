const socket = io();

socket.on('connect', () => {
    console.log("소켓 연결 성공");
});

socket.on('enter', (data) => {
    cars.push(data.enterCar);
    setCarTimer();
});

socket.on('out', (data) => {
    const itemToFind = cars.find((item) => {return item[id] === data.id});
    const idx = cars.indexOf(itemToFind);
    if(idx > -1) cars.splice(idx, 1);

    let aTag = document.createElement("a");
    aTag.classList.add("waves-effect waves-light btn");
    aTag.innerHTML = "확인";
    aTag.onclick = () => {
        const table = document.getElementById(`u${data.id}`);
        table.parentNode.removeChild(table);
    }
    const out = document.querySelector(`u${data.id} > .out`);
    out.innerHTML = "";
    out.appendChild(aTag);
    setCarTimer();
});
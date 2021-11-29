const socket = io();

const carTable = document.getElementById("carTable");

socket.on('connect', () => {
    console.log("소켓 연결 성공");
});

socket.on('enter', (data) => {
    const tr = document.createElement("tr");
    tr.id = `u${data.data.id}`;

    const idx = document.createElement("td");
    const uid = document.createElement("td");
    const number = document.createElement("td");
    const enter_time = document.createElement("td");
    const nowTime = document.createElement("td");
    const nowPrice = document.createElement("td");
    const out = document.createElement("td");

    idx.innerHTML = cars.length + 1;
    uid.innerHTML = data.data.id;
    number.innerHTML = data.data.number;
    enter_time.innerHTML = data.data.enter_time;
    out.innerHTML = "주차 중";

    nowTime.classList.add("nowTime");
    nowPrice.classList.add("nowPrice");

    tr.append(idx);
    tr.append(uid);
    tr.append(number);
    tr.append(enter_time);
    tr.append(nowTime);
    tr.append(nowPrice);
    tr.append(out);

    carTable.append(tr);

    cars.push(data.data);
    setCarTimer();
});

socket.on('out', (data) => {
    const itemToFind = cars.find((item) => {return item.id === data.id});
    const idx = cars.indexOf(itemToFind);
    if(idx > -1) cars.splice(idx, 1);

    let aTag = document.createElement("a");
    aTag.classList.add("waves-effect", "waves-light", "btn");
    aTag.innerHTML = "확인";
    aTag.onclick = () => {
        const table = document.getElementById(`u${data.id}`);
        table.parentNode.removeChild(table);
        socket.emit('out', {id: data.id});
    }
    const out = document.querySelector(`#u${data.id} > .out`);
    out.innerHTML = "";
    out.append(aTag);

    setCarTimer();
});

socket.on('err', (data) => {
    console.log(data.msg);
});
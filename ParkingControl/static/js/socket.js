const socket = io();  // 소켓 서버와 연결

const carTable = document.getElementById("carTable");   // 차량 목록 테이블 불러오기

socket.on('connect', () => {
    console.log("소켓 연결 성공");  //소켓 연결 성공 할 때
});

socket.on('enter', (data) => {  // 차량이 들어올 떄 차량 번호와 들어온 시간을 timestamp 형식으로 서버에서 받아온다.
    const tr = document.createElement("tr");
    tr.id = `u${data.data.id}`;  // 차량 컬럼에 고유 아이디 부여

    const idx = document.createElement("td");            // 주차된 차량의 인덱스 표시
    const uid = document.createElement("td");            // 차량의 고유 아이이 표시
    const number = document.createElement("td");         // 차량 번호 표시
    const enter_time = document.createElement("td");     // 들어온 시간 표시
    const nowTime = document.createElement("td");        // 주차 경과 시간 표시
    const nowPrice = document.createElement("td");       // 현재 주차 요금 표시
    const out = document.createElement("td");            // 주차 상태 여부 표시

    idx.innerHTML = cars.length + 1;
    uid.innerHTML = data.data.id;
    number.innerHTML = data.data.number;
    enter_time.innerHTML = data.data.enter_time;
    nowPrice.innerHTML = "0 원";
    out.innerHTML = "주차 중";

    nowTime.classList.add("nowTime");
    nowPrice.classList.add("nowPrice");
    out.classList.add("out");

    tr.append(idx);
    tr.append(uid);
    tr.append(number);
    tr.append(enter_time);
    tr.append(nowTime);
    tr.append(nowPrice);
    tr.append(out);   // 컬럼에 추가

    carTable.append(tr);   // 테이블에 컬럼 추가

    cars.push(data.data);  // 타이머를 위한 cars 배열에 새로 추가
    setCarTimer();  // 타이머 새로 갱신
});

socket.on('out', (data) => {   // 차량이 나갈 때  (이미 주차된 차량번호와 동일한 번호판일때)
    const itemToFind = cars.find((item) => {return item.id === data.id});  // 객체배열에서 나갈 차량 검색
    const idx = cars.indexOf(itemToFind);
    if(idx > -1) cars.splice(idx, 1);  // 나가는 차량의 타이머를 멈추기 위해 cars 배열에서 삭제

    let aTag = document.createElement("a");
    aTag.classList.add("waves-effect", "waves-light", "btn");
    aTag.innerHTML = "확인";   // 결제 될 때 확인 버튼 눌러서 데이터베이스에서 삭제
    aTag.onclick = () => {    // 확인 버튼을 눌렀을 때
        const table = document.getElementById(`u${data.id}`);
        table.parentNode.removeChild(table);  // 테이블에서 컬럼 삭제
        socket.emit('out', {id: data.id});  // 데이터베이스 삭제 요청
    }
    const out = document.querySelector(`#u${data.id} > .out`);  // 상태여부 선택
    
    out.innerHTML = "";
    out.append(aTag);  // 확인 버튼 추가

    setCarTimer();  // 타이머 새로 갱신
});

socket.on('err', (data) => {  // 서버에서 에러 날 떄
    console.log(data.msg);  // 에러 메세지 출력
});

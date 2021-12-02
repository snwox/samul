let carTimer = [];  // 주차 경과 시간과 요금을 바로 바꾸기 위해 미리 selector를 저장할 변수

function setCarTimer() {
    if(Timer !== undefined) clearInterval(Timer);  // 새로 갱신 될 때 타이머를 멈춤
    
    carTimer = [];  // 새로 초기화

    for(let i of cars) {  // cars 변수에 들어있는 배열들을 하나씩 넣음
        carTimer.push({
            carTimeTable: document.querySelector(`#u${i.id} > .nowTime`),  // 경과 시간 변경하기 위한 dom
            carFeeTable: document.querySelector(`#u${i.id} > .nowPrice`),  // 요금 값을 변경하기 위한 dom
            enterTime: i.enter_timeS  // 경과시간을 계산하기 위한 차가 들어올 때의 timestamp
        });
    }
    if(carTimer.length === 0) return;  // 차량이 아무것도 없으면 타이머 실행 안함  (최적화 목적)
    
    Timer = setInterval(() => {  // 1초씩 반복
        for(let car of carTimer) {
            const now = new Date();
            const enter = new Date(car.enterTime);
            const time = now - enter;
    
            const day = Math.floor(time / (1000 * 60 * 60 * 24));        // 경과시간의 일
            const hour = Math.floor(((time / (1000 * 60 *60 )) % 24 ));  // 경과시간의 시간
            const minute = Math.floor(((time / (1000 * 60 )) % 60 ));    // 경과시간의 분
            const seconds = Math.floor((time / 1000 ) % 60);             // 경과시간의 초
    
            car.carTimeTable.innerHTML = `${day}일 ${hour}시 ${minute}분 ${seconds}초`;  // 경과시간 표시
            car.carFeeTable.innerHTML = `${Math.floor(time / 1000)} 원`;  // 현재 요금 표시  (1초에 1원)
        }
    }, 1000);
};

setCarTimer();  // 새로 load 되면 함수 실행

// using k6 load testing

// https://grafana.com/docs/k6/latest/using-k6/http-requests/

import http from 'k6/http';
import { check } from 'k6';

export const options = {
// Case 1:
//vus: 10,
//duration: 10s,

// Case 2:
vus: 100,
stages: [
    { duration: '15s', target: 100 }, // ramp up
    { duration: '15s', target: 100 }, // stable
    { duration: '45s', target: 1000 }, // spike - stress test
    { duration: '1m', target: 0 }, // ramp down
  ],
  thresholds: {
    // 90% of requests must finish within 500ms.
//    http_req_duration: ['p(90) < 500'],
//    http_req_duration: ['p(90) < 400', 'p(95) < 800', 'p(99.9) < 2000'],

    // During the whole test execution, the error rate must be lower than 1%.
//    http_req_failed: ['rate<0.5'],
  },
};

export default function () {
// let allows for declaring block-scoped variables. You cannot use let to redeclare a variable, whereas you can with var in js.
// for async endpoint
  let res = http.get('http://127.0.0.1:8000/hasync');
// for sync endpoint
//  let res = http.get('http://127.0.0.1:8000/hsync');

  check(res, {
    'api status in load test is 200': (r) => r.status === 200,
  });
}
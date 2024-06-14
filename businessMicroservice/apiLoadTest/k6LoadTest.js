// using k6 load testing - for Task4
// Reference: https://grafana.com/docs/k6/latest/using-k6/http-requests/

import http from 'k6/http';
import { check } from 'k6';

export const options = {
// Case 1:
//vus: 10,
//duration: 10s,

// Case 2: Simple stress test
vus: 10,
stages: [
    { duration: '1s', target: 10 }, // ramp up
    { duration: '3s', target: 15 }, // stable
    { duration: '5s', target: 30 }, // spike - stress test
    { duration: '1m', target: 0 }, // ramp down
  ],
  thresholds: {
//    http_req_duration: ['p(90) < 500'], //90% of requests must finish within 500ms.
//    http_req_duration: ['p(90) < 400', 'p(95) < 800', 'p(99.9) < 2000'], // similar conditions
//    http_req_failed: ['rate<0.5'], // During the whole test execution, the error rate must be lower than 1%.
  },
};

export default function () {
// for async endpoint
//  let res = http.get('http://127.0.0.1:8000/asyncrpstatus'); // let keyword allows for declaring block-scoped variables. You cannot use let to redeclare a variable, whereas you can with var in js.
// for sync endpoint
  let res = http.get('http://127.0.0.1:8000/syncrpstatus');
  check(res, {
    'api status in load test is 200': (r) => r.status === 200,
  });
}

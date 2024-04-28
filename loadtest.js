// using k6 load testing

// https://grafana.com/docs/k6/latest/using-k6/http-requests/

import http from 'k6/http';
import { check } from 'k6';

export const options = {
  thresholds: {
    // 90% of requests must finish within 500ms.
//    http_req_duration: ['p(90) < 500'],
//    http_req_duration: ['p(90) < 400', 'p(95) < 800', 'p(99.9) < 2000'],

    // During the whole test execution, the error rate must be lower than 1%.
//    http_req_failed: ['rate<0.5'],
  },
};

export default function () {
  http.get('http://127.0.0.1:8000/hasync');
  check(res, {
    'api status in load test is 200': (r) => r.status === 200,
  });
}
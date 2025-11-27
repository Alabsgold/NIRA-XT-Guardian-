import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    vus: 10,
    duration: '30s',
};

export default function () {
    // Test Backend Policy API
    const res = http.get('http://localhost:8000/api/policy/1');
    check(res, { 'status was 200': (r) => r.status == 200 });
    sleep(1);
}

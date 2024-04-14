import { createClient } from 'redis';

//const client = createClient({ url: 'redis://cache:6379' });
const client = createClient();



client.on('error', err => console.log('Redis Client Error', err));

await client.connect();

await client.set('foo', '42');
const value = await client.get('foo');

console.log(value)
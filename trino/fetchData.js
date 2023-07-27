/* (async () => {
  let response = await fetch('http://localhost:8080/v1/statement', {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    redirect: "follow",
    referrerPolicy: "no-referrer",
    body: "select *, now() from tpch.sf1.orders  order by orderkey asc limit 3",
    headers: {
      //'X-Trino-User': 'root',
      'X-Trino-Catalog': 'tpch',
      'X-Trino-Schema': 'sf1',
      'accept': 'application/json',
      'Authorization': 'Basic root'        
    }
  })
  
  let d = await response.json();  
  if (d.nextUri) drainTrino(d.nextUri);
  
})(); */

let body = 'select *, now() from tpch.sf1.orders  order by orderkey asc limit 3';
(async () => {
  const orders = await drainTrino('http://localhost:8080/v1/statement', 'POST', body);
  console.log('from root', orders)
})();

async function drainTrino(nextUri, verb, body) {
    let option = {
      method: verb,
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: body,
      headers: {
        'accept': 'application/json',
        'Authorization': 'Basic root'
      }
    };

    if (body) {
      option.body = body
    };

    let response = await fetch(nextUri, option);
    let d = await response.json();
    let orders = [];
    if (d.data && d.columns) {
  
      orders = d.data.map(item => {
        let o = {};
        o["orderkey"] = item[0].toString();
        o[`clerk`] = item[6];
        o[`totalprice`] = item[3];
        o[`orderdate`] = item[4];
        return o;
      })
  
    }
    if (d.nextUri) {
      const nextOrders = await drainTrino(d.nextUri, 'GET')
      return [...orders, ...nextOrders];
    } else {      
      return orders
    }
  } 
let orders = [];

(async () => {
  let response = await fetch('http://localhost:8080/v1/statement', {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    redirect: "follow",
    referrerPolicy: "no-referrer",
    body: "select *, now() from tpch.sf1.orders  order by orderkey asc limit 20",
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
  
})();


async function drainTrino(nextUri) {
  let final;
  let response = await fetch(nextUri,
    {
      method: "GET",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      redirect: "follow",
      referrerPolicy: "no-referrer",
      headers: {
        'accept': 'application/json',
        'Authorization': 'Basic root'        
      }        
    }
  )
  let d = await response.json();
  
  if (d.nextUri) {
    
    if (d.data  && d.columns) {
      let o = {};
      for (let i = 0; i < d.data.length; i++) {
        o["orderkey"] = d.data[i][0].toString();
        o[`clerk`] = d.data[i][6];
        o[`totalprice`] = d.data[i][3];
        o[`orderdate`] = d.data[i][4];        
        orders.push(o)
      } 
      await drainTrino(d.nextUri);      
    }    
  }
  console.log('orders', orders)
  return orders;
}




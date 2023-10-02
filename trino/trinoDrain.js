(async () => {
    const orders = await drainTrino('http://localhost:8080/v1/statement');
    console.log('orders', orders)
})();


async function drainTrino(nextUri) {
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
      const nextOrders = await drainTrino(d.nextUri)
      return [...orders, ...nextOrders];
    } else {
      return orders
    }
  } 
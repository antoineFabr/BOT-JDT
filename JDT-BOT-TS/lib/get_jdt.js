export async function getJDT(url){
  try {
    const res = await fetch(url);
    if(res.status == 200) {
      const tab = await res.text();
      const pattern = /google\.visualization\.Query\.setResponse\((.*)\);/;
      const match = tab.match(pattern)

      if(match && match[1]) {
        const json_str = match[1];
        const data = JSON.parse(json_str);
        return data;
      }
    }
    return null;
  } catch(e){
    console.error("erreur lors du fetch : ", e)
    return e;
  }
}
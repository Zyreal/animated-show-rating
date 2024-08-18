import React, {useState} from 'react'

function App() {
    const [show, setShow] = useState("")
    const [score, setScore] = useState({
      showImage: "N/A",
      mal: "",
      anilist: "",
      livechart: "",
      animeName: "",
    })
    function handleShowChange(e) {
        setShow(e.target.value)
    }
    const handleSubmit = async(e) => {
        // send to python script
        fetch("/search/" + show).then((res) =>
        res.json().then((score) =>{
          setScore({
            showImage: score.animeImage,
            mal: score.MAL,
            anilist: score.Anilist,
            livechart: score.Livechart,
            animeName: score.name,
          })
        }))
        setShow("")
        e.preventDefault()
    }

  return (<div className="flex flex-col m-auto">
    <form onSubmit={handleSubmit} className="m-auto mt-10">
        <input className="border-2 border-black rounded-md pl-2" value={show} onChange={handleShowChange}/>
    </form>
    {score.animeName == "" ? <></> : <>
      <div className="m-auto mt-4 mb-4 text-6xl font-serif">{score.animeName}</div>
      <div className="flex h-[80vh] pr-10 justify-center" >
        <div className="left flex w-1/2 m-auto h-full">
          <img className="m-auto h-full rounded-lg" src={score.showImage} alt=''></img>
        </div>
        <div className="right w-1/2 h-full flex flex-col m-auto">
          <div className="mal m-auto ml-3 flex">
            <img className="rounded-md" width={100} height={100} src="https://play-lh.googleusercontent.com/zVwzSU7ozKU0x78V7zYWDw2XFjgGsBBJA_qIJQXAFnS1R3VemFbpdaV9Bm3zOTTHvXw" alt="MAL img"></img>
            <div className="m-auto ml-6 text-4xl font-mono" >MAL: {score.mal}</div>
          </div>
          <div className="anilist m-auto ml-3 flex">
            <img className="rounded-md" width={100} height={100} src="https://anilist.co/img/icons/android-chrome-512x512.png" alt="Anilist img"></img>
            <div className="m-auto ml-6 text-4xl font-mono">Anilist: {score.anilist}</div>
          </div>
          <div className="livechart m-auto ml-3 flex">
            <img className="rounded-md" width={100} height={100} src="https://play-lh.googleusercontent.com/VKmSCct1e0voOG-N9H504heV_lIwO4VrgFBywbiNH_Hm66wZ2IprbWfbWTmc19laF78G" alt="Livechart img"></img>
            <div className="m-auto ml-6 text-4xl font-mono">Livechart: {score.livechart}</div>
          </div>
        </div>
      </div>
      </>}
  </div>
  )
}

export default App
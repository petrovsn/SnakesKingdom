import { useEffect, useState } from "react";
import * as game_controller from "./controllers/game_controller.js";
import GameViewer from "./widgets/GameViewer.jsx";
import RawGameDataViewer from "./widgets/RawGameDataViewer.jsx";
import PlayersTable from "./widgets/PlayersTable.jsx";
import CreateRoomWidget from "./widgets/CreateRoomWidget.jsx";


function App() {
    const [isConnected, setIsConnected] = useState(false);
    useEffect(() => {
        if (!isConnected) {
            return;
        }

        const handleKeyDown = (event) => {
            console.log(
                "KEY:",
                event.key,
                "CODE:",
                event.code
            );

            const commands = {
                ArrowUp: "up",
                ArrowDown: "down",
                ArrowLeft: "left",
                ArrowRight: "right",

                KeyW: "up",
                KeyA: "left",
                KeyS: "down",
                KeyD: "right",
            };

            const command = commands[event.code];

            if (!command) {
                return;
            }

            event.preventDefault();

            game_controller.send_command(command);
        };

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
            game_controller.disconnect();
        };
    }, [isConnected]);


  return (
    <div>
      <CreateRoomWidget
        onCreated={(result) => {
          console.log("Room created:", result);
        }}
      />

      <PlayersTable />
      <GameViewer />
      <RawGameDataViewer />

    </div>
  );
}


export default App;
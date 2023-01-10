using System.Collections.Generic;
using System;

namespace MessengerWeb.Client.Services
{
    public class Settings
    {
        public List<EngineEntity> Engines { get; set; }

        public Settings()
        {
            Engines = new List<EngineEntity> 
            {
                new EngineEntity()
                {
                    Engine = Engine.Luna,
                    Name = "Vision Labs Platform",
                    UUID = "2a2a5e3b-29c6-426f-97cc-d9e1fb701ad3",
                    IsSelected = true,
                },
                new EngineEntity()
                {
                    Engine = Engine.Ntech,
                    Name = "NTech Platform",
                    UUID = "6cf3b728-4cf9-4262-b4b2-315c019515de",
                    IsSelected = false,
                },
                new EngineEntity()
                {
                    Engine = Engine.Tevian,
                    Name = "Tevian Platform",
                    UUID = "3aac91d1-319f-46d8-bd52-35693457f498",
                    IsSelected = false,
                },
                new EngineEntity()
                {
                    //Facenet and tevian are have the same API
                    Engine = Engine.Tevian, 
                    Name = "Facenet (ours)",
                    UUID = "d733c7a4-7da4-47d4-aa25-289b9a479819",
                    IsSelected = false,
                },
            };
        }
    }
}

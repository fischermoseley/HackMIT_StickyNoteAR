using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Platformer.Gameplay;
using Platformer.Model;
using Platformer.Core;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class ReceiveData : MonoBehaviour
{
    // Start is called before the first frame update
    
    Thread receiveThread;
    UdpClient client;
    int port;
    bool connected;

    /// <summary>
    /// Receive data via UDP
    /// </summary>
    private void InitUDP()
    {
        print("UDP Recceiver initialized");
        receiveThread = new Thread (new ThreadStart(DataReceiver));
        receiveThread.IsBackground = true; 
        receiveThread.Start ();

    }

    private void DataReceiver()
    {
        client = new UdpClient (port);
        while (true)
        {
            try
            {   
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port);
                byte[] data = client.Receive(ref anyIP);

                string text = Encoding.UTF8.GetString(data);

                if (text && !connected)
                {
                    print("connected to UDP!");
                    connected = true;
                }

                print (">> " + text);

            } catch(Exception e)
            {
                print (e.ToString());
            }
        }
    }
    void Start()
    {
        port = 6150;
        InitUDP();

    }

    // Update is called once per frame
    void Update()
    {
        if (!connected)
        {
            print("not yet connected to udp");
        }
    }
}

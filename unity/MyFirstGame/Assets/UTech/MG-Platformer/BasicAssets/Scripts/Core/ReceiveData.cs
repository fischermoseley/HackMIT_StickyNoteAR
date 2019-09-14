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

    /// <summary>
    /// Receive data via UDP
    /// </summary>
    private void InitUDP()
    {
        print("UDP initialized");
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
        print("script is activating");
        InitUDP();

    }

    // Update is called once per frame
    void Update()
    {
        // base.update(); // Not sure if this is necessary
    }
}

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


public class SendData : MonoBehaviour
{
    private static int localPort;
     // prefs
    private string IP;  // define in init
    public int port;  // define in init
    
    public bool connected;

    // "connection" things
    IPEndPoint remoteEndPoint;
    UdpClient client;

    // if we want to call it from shell (as program)
    // private static void Main()
    // {
    //     UDPSend sendObj=new UDPSend();
    //     sendObj.init();
    // }
   
    // Start is called before the first frame update
    void Start()
    {
        print("sending script activated");
        init();
    }

    public void init()
    {
        IP="127.0.0.1";
        port=6150;
        connected = false;

        remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), port);
        client = new UdpClient();

        //run initial handshake to detect if it's working or not
        sendString("hello");

        print("Sending to "+IP+" : "+port);
        print("Testing: nc -lu "+IP+" : "+port);
   
    }

    // sendData
    private void sendString(string message)
    {
        print("sending new message");
        try
        {
            byte[] data = Encoding.UTF8.GetBytes(message);
            client.Send(data, data.Length, remoteEndPoint);
        }
        catch (Exception err)
        {
            print(err.ToString());
        }
    }

    void OnGUI()
    {
        if (Input.GetKeyDown("u"))
        {   
            sendString("calibrate");
        }

        if (Input.GetKeyDown("left ctrl"))
        {
            sendString("sticky");
        }
    }
    // Update is called once per frame
    void Update()
    {
        if (connected == false)
        {
           // print("can't connect to opencv");
        }
    }
}

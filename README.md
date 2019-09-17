![StickyAR](https://github.com/FischerMoseley/HackMIT_StickyNoteAR/blob/master/assets/gamelogos/Logo.png)

## Demo!
![Recorded Demo](https://github.com/FischerMoseley/HackMIT_StickyNoteAR/blob/master/assets/gameplay.gif)

## Awarded Best in Entertainment Category
![Award Ceremony](https://github.com/FischerMoseley/HackMIT_StickyNoteAR/blob/master/assets/award.png)

## Inspiration
Virtually every classroom has a projector, whiteboard, and sticky notes. With OpenCV and Python being more accessible than ever, we wanted to create an augmented reality entertainment platform that any enthusiast could learn from and bring to their own place of learning. StickyAR is just that, with a super simple interface that can anyone can use to produce any tile-based Numpy game. Our first offering is StickyJump , a 2D platformer whose layout can be changed on the fly by placement of sticky notes. We want to demystify computer science in the classroom, and letting students come face to face with what's possible is a task we were happy to take on.

## What it does
StickyAR works by using OpenCV's Contour Recognition software to recognize the borders of a projector image and the position of human placed sticky notes. We then use a matrix transformation scheme to ensure that the positioning of the sticky notes align with the projector image so that our character can appear as if he is standing on top of the sticky notes. We then have code for a simple platformer that uses the sticky notes as the platforms our character runs, jumps, and interacts with!

## How we built it
We split our team of four into two sections, one half that works on developing the OpenCV/Data Transfer part of the project and the other half who work on the game side of the project. It was truly a team effort.

## Challenges we ran into
The biggest challenges we ran into were that a lot of our group members are not programmers by major. We also had a major disaster with Git that almost killed half of our project. Luckily we had some very gracious mentors come out and help us get things sorted out! We also first attempted to the game half of the project in unity which ended up being too much of a beast to handle.

## Accomplishments that we're proud of
That we got it done! It was pretty amazing to see the little square pop up on the screen for the first time on top of the spawning block. As we think more deeply about the project, we're also excited about how extensible the platform is for future games and types of computer vision features.

## What we learned
A whole ton about python, OpenCV, and how much we regret spending half our time working with Unity. Python's general inheritance structure came very much in handy, and its networking abilities were key for us when Unity was still on the table. Our decision to switch over completely to Python for both OpenCV and the game engine felt like a loss of a lot of our work at the time, but we're very happy with the end-product.

## What's next for StickyAR
StickyAR was designed to be as extensible as possible, so any future game that has colored tiles as elements can take advantage of the computer vision interface we produced. We've already thought through the next game we want to make - StickyJam. It will be a music creation app that sends a line across the screen and produces notes when it strikes the sticky notes, allowing the player to vary their rhythm by placement and color.

Built With OpenCV, Pygame, and Python

Made by Zach Rolfness, Tim Gutterman, Lucas Igel, Fischer Moseley in 24 hours for HackMIT 2019.
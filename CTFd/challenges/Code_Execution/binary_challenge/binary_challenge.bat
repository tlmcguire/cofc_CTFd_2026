@echo off
setlocal enabledelayedexpansion

REM Generate a random number between 1 and 1000
set /a target=%random% %% 1000 + 1

echo Welcome to the Binary Search Game!
echo I'm thinking of a number between 1 and 1000.

REM Limit the player to 10 guesses
set /a MAX_GUESSES=10
set /a guess_count=0

:game_loop
if %guess_count% geq %MAX_GUESSES% goto game_over

set /p guess=Enter your guess: 

REM Validate that the input is a number
for /f "delims=0123456789" %%A in ("%guess%") do (
    echo Please enter a valid number.
    goto game_loop
)

set /a guess_count+=1

if %guess% lss %target% (
    echo Higher! Try again.
) else if %guess% gtr %target% (
    echo Lower! Try again.
) else (
    echo Congratulations! You guessed the correct number: %target%
    REM Retrieve the flag from the flag file
    type ..\..\flags\binary_flag.txt
    exit /b 0
)

goto game_loop

:game_over
echo Sorry, you've exceeded the maximum number of guesses.
exit /b 1

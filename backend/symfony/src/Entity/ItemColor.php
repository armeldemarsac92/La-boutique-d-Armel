<?php

namespace App\Entity;

use App\Repository\ItemColorRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: ItemColorRepository::class)]
class ItemColor
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private ?string $color_name = null;

    #[ORM\Column(length: 255)]
    private ?string $color_hex = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function setId(int $id): static
    {
        $this->id = $id;

        return $this;
    }

    public function getColorName(): ?string
    {
        return $this->color_name;
    }

    public function setColorName(string $color_name): static
    {
        $this->color_name = $color_name;

        return $this;
    }

    public function getColorHex(): ?string
    {
        return $this->color_hex;
    }

    public function setColorHex(string $color_hex): static
    {
        $this->color_hex = $color_hex;

        return $this;
    }
}

<?php

namespace App\Entity;

use App\Repository\CatalogRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: CatalogRepository::class)]
class Catalog
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private ?string $name = null;

    #[ORM\Column]
    private ?int $size_group_id = null;

    #[ORM\Column]
    private ?int $item_count = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function setId(int $id): static
    {
        $this->id = $id;

        return $this;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): static
    {
        $this->name = $name;

        return $this;
    }

    public function getSizeGroupId(): ?int
    {
        return $this->size_group_id;
    }

    public function setSizeGroupId(int $size_group_id): static
    {
        $this->size_group_id = $size_group_id;

        return $this;
    }

    public function getItemCount(): ?int
    {
        return $this->item_count;
    }

    public function setItemCount(int $item_count): static
    {
        $this->item_count = $item_count;

        return $this;
    }
}
